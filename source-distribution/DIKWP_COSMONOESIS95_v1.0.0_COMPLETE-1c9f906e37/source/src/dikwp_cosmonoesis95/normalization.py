from __future__ import annotations

import re
from typing import Any, Iterable

from .registries import load_registry, ontology_anchor_map
from .utils import cosine, l1_distance, normalize_text, normalize_weights, stable_id, top_items


def _tokens(text: str) -> set[str]:
    value = normalize_text(text).lower()
    latin = re.findall(r"[a-z][a-z0-9āīūṛṃḥṣṭḍñṅōē'\-]+", value)
    chinese = re.findall(r"[\u3400-\u9fff]{1,8}", value)
    grams: set[str] = set(latin)
    for chunk in chinese:
        if len(chunk) <= 4:
            grams.add(chunk)
        else:
            grams.update(chunk[i:i+n] for n in (1, 2, 3, 4) for i in range(len(chunk)-n+1))
    return {x for x in grams if x.strip()}


_KEYWORD_ANCHORS: dict[str, tuple[str, ...]] = {
    "D.EVENT": ("发生", "事件", "experience", "event", "revelation", "显现"),
    "D.SENSATION": ("感知", "感觉", "觉受", "sensation", "perception", "pain", "苦乐"),
    "D.OBSERVATION": ("观察", "见证", "经验", "observation", "witness", "testimony"),
    "D.BODY": ("身体", "物质", "生命", "气", "炁", "body", "matter", "embodied", "life"),
    "D.HISTORY": ("历史", "祖先", "谱系", "传承", "history", "lineage", "genealogy", "memory"),
    "I.DIFFERENCE": ("差异", "辨别", "二元", "difference", "distinction", "discernment"),
    "I.RELATION": ("关系", "互依", "缘起", "盟约", "合一", "relation", "interdependence", "covenant", "communion"),
    "I.PATTERN": ("模式", "秩序", "理", "节律", "pattern", "order", "rhythm", "symbol"),
    "I.BOUNDARY": ("边界", "身份", "自他", "洁净", "boundary", "identity", "self-other", "purity"),
    "I.CONTEXT": ("语境", "视角", "二谛", "尺度", "context", "perspective", "scale"),
    "I.TRANSLATION": ("翻译", "对齐", "诠释", "translation", "alignment", "interpretation"),
    "K.CONCEPT": ("概念", "范畴", "教义", "concept", "category", "doctrine"),
    "K.CAUSE": ("因果", "生成", "缘起", "创造", "cause", "generation", "creation", "emergence"),
    "K.WORLD_MODEL": ("宇宙", "终极实在", "神", "上帝", "天主", "真主", "创造者", "梵", "道", "世界", "cosmos", "universe", "god", "allah", "creator", "brahman", "dao", "tawhid"),
    "K.SELF_MODEL": ("自我", "灵魂", "无我", "心", "意识", "self", "soul", "no-self", "mind", "consciousness"),
    "K.REGULARITY": ("规律", "真理", "法", "logos", "asha", "truth", "law", "regularity"),
    "K.PRACTICE": ("修行", "仪式", "祈祷", "冥想", "礼", "practice", "ritual", "prayer", "meditation"),
    "K.META": ("反思", "空性", "无明", "否证", "修订", "reflection", "emptiness", "ignorance", "falsification", "revision"),
    "W.VALENCE": ("苦", "乐", "爱", "慈悲", "敬畏", "suffering", "joy", "love", "compassion", "awe"),
    "W.NORM": ("伦理", "义", "善", "戒", "诫命", "justice", "ethics", "duty", "virtue", "commandment"),
    "W.CONSEQUENCE": ("后果", "责任", "业", "审判", "consequence", "responsibility", "karma", "judgment"),
    "W.TRADEOFF": ("权衡", "中道", "平衡", "互补", "tradeoff", "middle way", "balance", "complementarity"),
    "W.MEANING": ("意义", "智慧", "神圣", "meaning", "wisdom", "sacred"),
    "W.LEGITIMACY": ("授权", "权威", "盟约", "尊严", "legitimacy", "authority", "consent", "dignity"),
    "P.INTENTION": ("意图", "愿", "信", "祈愿", "intention", "vow", "faith", "aspiration"),
    "P.LIBERATION": ("解脱", "救赎", "涅槃", "觉悟", "liberation", "salvation", "nirvana", "awakening"),
    "P.HARMONY": ("和谐", "正道", "自然", "无为", "harmony", "alignment", "naturalness"),
    "P.COMMUNION": ("合一", "临在", "亲近", "奉爱", "崇拜", "礼拜", "communion", "union", "presence", "devotion", "worship"),
    "P.FLOURISHING": ("繁荣", "修复", "和平", "共同善", "flourishing", "repair", "peace", "common good"),
    "P.AGENCY": ("行动", "选择", "自由", "拒绝", "agency", "choice", "freedom", "refusal"),
    "P.VERIFICATION": ("检验", "实践", "悔改", "校准", "verification", "experiment", "repentance", "calibration"),
    "P.CONTINUITY": ("连续", "传承", "后代", "永生", "continuity", "transmission", "future generations", "eternal life"),
}


def _concept_index() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for tradition in load_registry("traditions")["traditions"]:
        for concept in tradition.get("concepts", []):
            keys = [concept.get("term", ""), concept.get("gloss_cn", ""), concept.get("gloss_en", ""), *concept.get("aliases", [])]
            out.append({
                "tradition_id": tradition["id"],
                "tradition_name_cn": tradition["name_cn"],
                "family": tradition["family"],
                "concept": concept,
                "keys": [normalize_text(x).lower() for x in keys if normalize_text(x)],
                "tokens": set().union(*(_tokens(x) for x in keys if normalize_text(x))),
            })
    return out


def centroid(vectors: Iterable[dict[str, float]], weights: Iterable[float] | None = None) -> dict[str, float]:
    vector_list = list(vectors)
    if not vector_list:
        raise ValueError("At least one vector is required")
    weight_list = list(weights) if weights is not None else [1.0] * len(vector_list)
    if len(weight_list) != len(vector_list):
        raise ValueError("weights and vectors must have the same length")
    combined: dict[str, float] = {}
    for vector, weight in zip(vector_list, weight_list):
        for key, value in vector.items():
            combined[key] = combined.get(key, 0.0) + float(value) * float(weight)
    return normalize_weights(combined, set(ontology_anchor_map()))


def normalize_concept(term: str, *, context: str = "", tradition_id: str | None = None, top_k: int = 6) -> dict[str, Any]:
    term_n = normalize_text(term)
    if not term_n:
        raise ValueError("term must not be empty")
    query = normalize_text(f"{term_n} {context}").lower()
    query_tokens = _tokens(query)
    matches: list[tuple[float, dict[str, Any]]] = []
    for entry in _concept_index():
        if tradition_id and entry["tradition_id"] != tradition_id:
            continue
        exact = term_n.lower() in entry["keys"]
        overlap = len(query_tokens & entry["tokens"])
        union = len(query_tokens | entry["tokens"]) or 1
        score = (1.0 if exact else 0.0) + overlap / union
        if score > 0:
            matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1]["tradition_id"], item[1]["concept"]["term"]))

    if matches and matches[0][0] >= 0.25:
        selected = matches[:max(1, top_k)]
        max_score = selected[0][0]
        # Exact term matches are preserved as context-conditioned alternatives and then normalized into one centroid.
        relevant = [item for item in selected if item[0] >= max(0.30, max_score * 0.55)]
        if not relevant:
            relevant = selected[:1]
        vectors = [item[1]["concept"]["vector"] for item in relevant]
        weights = [item[0] for item in relevant]
        vector = centroid(vectors, weights)
        confidence = min(0.98, 0.55 + 0.25 * max_score + 0.05 * min(len(relevant), 3))
        method = "registry_exact_or_contextual_alignment"
        candidates = [{
            "tradition_id": entry["tradition_id"],
            "tradition_name_cn": entry["tradition_name_cn"],
            "term": entry["concept"]["term"],
            "gloss_cn": entry["concept"]["gloss_cn"],
            "match_score": round(score, 6),
            "vector": entry["concept"]["vector"],
            "mapping_note_cn": entry["concept"].get("mapping_note_cn", ""),
        } for score, entry in relevant]
    else:
        weighted: dict[str, float] = {}
        lowered = query.lower()
        for anchor, keywords in _KEYWORD_ANCHORS.items():
            count = sum(1 for keyword in keywords if keyword.lower() in lowered)
            if count:
                weighted[anchor] = weighted.get(anchor, 0.0) + count
        if not weighted:
            # Full semantic closure: novelty is placed inside DIKWP as a provisional concept/context/translation object.
            weighted = {
                "I.CONTEXT": 1.0,
                "I.TRANSLATION": 1.0,
                "K.CONCEPT": 3.0,
                "K.META": 2.0,
                "W.MEANING": 1.0,
                "P.VERIFICATION": 1.0,
            }
            method = "provisional_in_space_extension"
            confidence = 0.25
        else:
            weighted.setdefault("I.CONTEXT", 0.5)
            weighted.setdefault("K.CONCEPT", 0.5)
            weighted.setdefault("P.VERIFICATION", 0.25)
            method = "keyword_in_space_projection"
            confidence = min(0.70, 0.30 + 0.06 * sum(weighted.values()))
        vector = normalize_weights(weighted, set(ontology_anchor_map()))
        candidates = []

    anchors = ontology_anchor_map()
    return {
        "normalization_id": stable_id("norm", {"term": term_n, "context": context, "tradition": tradition_id, "vector": vector}),
        "input": {"term": term_n, "context": normalize_text(context), "tradition_id": tradition_id},
        "method": method,
        "vector": vector,
        "top_coordinates": [{"id": key, "weight": value, "label_cn": anchors[key]["label_cn"], "label_en": anchors[key]["label_en"]} for key, value in top_items(vector, 10)],
        "candidate_source_mappings": candidates,
        "confidence": round(confidence, 6),
        "normalization_status": "complete_in_dikwp_space",
        "out_of_space_residual": 0.0,
        "historical_identity_claim": False,
        "translation_loss_cn": "差异已表示在空间内的坐标权重、语境与候选来源中；低置信度表示需要更多语境，不表示存在空间外不可互译对象。",
        "automatic_external_action_authority": 0,
    }


def compare_vectors(a: dict[str, float], b: dict[str, float]) -> dict[str, Any]:
    diff = {key: round(a.get(key, 0.0) - b.get(key, 0.0), 12) for key in sorted(set(a) | set(b))}
    positives = sorted(((k, v) for k, v in diff.items() if v > 0), key=lambda x: -x[1])[:8]
    negatives = sorted(((k, -v) for k, v in diff.items() if v < 0), key=lambda x: -x[1])[:8]
    return {
        "cosine_similarity": round(cosine(a, b), 8),
        "l1_distance": round(l1_distance(a, b), 8),
        "a_more_weighted": [{"coordinate": k, "difference": round(v, 8)} for k, v in positives],
        "b_more_weighted": [{"coordinate": k, "difference": round(v, 8)} for k, v in negatives],
        "difference_vector": diff,
        "difference_is_inside_dikwp_space": True,
        "equivalence_claim": False,
    }


def compare_concepts(term_a: str, term_b: str, *, context_a: str = "", context_b: str = "", tradition_a: str | None = None, tradition_b: str | None = None) -> dict[str, Any]:
    a = normalize_concept(term_a, context=context_a, tradition_id=tradition_a)
    b = normalize_concept(term_b, context=context_b, tradition_id=tradition_b)
    return {
        "a": a,
        "b": b,
        "comparison": compare_vectors(a["vector"], b["vector"]),
        "interpretation_cn": "相似度表示在统一 DIKWP 坐标中的结构接近程度，不证明两个术语在历史、神学、本体或实践上完全同一。",
        "automatic_external_action_authority": 0,
    }
