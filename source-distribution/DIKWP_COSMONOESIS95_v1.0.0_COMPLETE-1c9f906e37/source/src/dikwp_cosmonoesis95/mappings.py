from __future__ import annotations

from typing import Any

from .normalization import centroid, compare_vectors
from .registries import load_registry, tradition_map
from .utils import top_items


def tradition_profiles() -> list[dict[str, Any]]:
    return load_registry("traditions")["traditions"]


def civilization_profiles() -> list[dict[str, Any]]:
    traditions = tradition_map()
    out: list[dict[str, Any]] = []
    for civ in load_registry("civilizations")["civilizations"]:
        members = [traditions[item] for item in civ["member_traditions"]]
        vector = centroid([item["profile_vector"] for item in members])
        out.append({
            **civ,
            "member_count": len(members),
            "profile_vector": vector,
            "top_coordinates": [{"coordinate": k, "weight": v} for k, v in top_items(vector, 10)],
            "normalization_status": "complete_in_dikwp_space",
            "out_of_space_residual": 0.0,
        })
    return out


def universal_centroid() -> dict[str, Any]:
    profiles = tradition_profiles()
    vector = centroid([item["profile_vector"] for item in profiles])
    return {
        "name_cn": "世界宗教—文明 DIKWP 归一重心",
        "vector": vector,
        "top_coordinates": [{"coordinate": k, "weight": v} for k, v in top_items(vector, 15)],
        "interpretation_cn": "该重心是计算性共同坐标，不是新的宗教权威、折衷教义或‘万教原本完全相同’的历史断言。",
        "out_of_space_residual": 0.0,
    }


def similarity_matrix(kind: str = "tradition") -> dict[str, Any]:
    if kind == "tradition":
        profiles = [{"id": x["id"], "name_cn": x["name_cn"], "vector": x["profile_vector"]} for x in tradition_profiles()]
    elif kind == "civilization":
        profiles = [{"id": x["id"], "name_cn": x["name_cn"], "vector": x["profile_vector"]} for x in civilization_profiles()]
    else:
        raise ValueError("kind must be tradition or civilization")
    rows = []
    for a in profiles:
        for b in profiles:
            rows.append({"a": a["id"], "b": b["id"], "similarity": round(compare_vectors(a["vector"], b["vector"])["cosine_similarity"], 8)})
    return {"kind": kind, "items": [{"id": p["id"], "name_cn": p["name_cn"]} for p in profiles], "matrix": rows}


def closest_pairs(kind: str = "tradition", limit: int = 25) -> list[dict[str, Any]]:
    profiles = tradition_profiles() if kind == "tradition" else civilization_profiles()
    pairs = []
    for i, a in enumerate(profiles):
        for b in profiles[i+1:]:
            comp = compare_vectors(a["profile_vector"], b["profile_vector"])
            pairs.append({
                "a": a["id"], "a_name_cn": a["name_cn"],
                "b": b["id"], "b_name_cn": b["name_cn"],
                "cosine_similarity": comp["cosine_similarity"],
                "l1_distance": comp["l1_distance"],
                "equivalence_claim": False,
            })
    pairs.sort(key=lambda x: (-x["cosine_similarity"], x["l1_distance"], x["a"], x["b"]))
    return pairs[:limit]
