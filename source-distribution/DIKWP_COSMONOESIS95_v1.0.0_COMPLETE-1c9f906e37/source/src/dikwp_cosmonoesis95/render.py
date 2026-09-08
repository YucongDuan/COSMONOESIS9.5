from __future__ import annotations

if __package__:
    from ._ui_presentation import localize_html as _ui_localize_html
else:
    from _ui_presentation import localize_html as _ui_localize_html


import json
from typing import Any

from .utils import html, top_items


def _pct(value: float) -> str:
    return f"{100 * float(value):.1f}%"


def render_report(bundle: dict[str, Any]) -> str:
    ontology = bundle["registries"]["ontology"]
    traditions = bundle["tradition_mappings"]
    civilizations = bundle["civilization_mappings"]
    audit = bundle["claim_audit"]
    assessments = bundle["consciousness_assessments"]
    consciousness_registry = bundle["registries"]["consciousness"]
    principles = bundle["registries"]["principles"]["principles"]
    source_lookup = {s["id"]: s for s in bundle["registries"]["evidence"]["sources"]}

    lines: list[str] = []
    lines += [
        "# DIKWP-COSMONOESIS 9.5 完整系统报告",
        "",
        "## 宇宙意识、宗教—文明语义归一、非规范材料审计与现实接触",
        "",
        f"- 编译标识：`{bundle['compilation_id']}`",
        f"- 版本：`{bundle['version']}`",
        f"- Mesh 模式：`{bundle['mesh_mode']}`",
        f"- 生成时间：`{bundle['generated_at']}`",
        "- 自动外部行动权限：`0`",
        "",
        "> 本系统所称“终极”，不是把某一物理理论、宗教教义或人工智能模型宣布为永恒最后真理，而是把来源、差异、价值、目的、替代世界模型、反证、现实返回、权利与可修订性尽可能纳入同一责任闭环。",
        "",
        "## 1. 对用户修正的落实：在 DIKWP 语义空间归一",
        "",
        "系统不把各宗教文明安置为彼此不可通约的孤岛，也不设置永久的‘不可翻译残差区’。所有原生概念、派别差异、新增概念和歧义都必须进入 D/I/K/W/P 坐标。原生术语仍保存为来源和校验入口，但不享有阻断比较的空间外特权。",
        "",
        "这里的归一是坐标归一，而不是把所有宗教改写成同一套历史教义：",
        "",
        "```text",
        "原生术语 + 派别 + 语境 + 来源",
        "              ↓ Φ",
        "       DIKWP 归一向量",
        "              ↓",
        "共同坐标上的相似、方向、层级、目的和后果差",
        "              ↓",
        "现实验证、修订与版本化扩展",
        "```",
        "",
        "差异向量 `x-y` 仍位于 DIKWP 空间之内；低置信度表示需要更多语境，而不是承认某个概念永远不可进入统一空间。",
        "",
        "## 2. 统一语义空间",
        "",
        "| 家族 | 核心问题 |",
        "|---|---|",
    ]
    for key in "DIKWP":
        family = ontology["families"][key]
        lines.append(f"| {key} · {family['cn']} | {family['question']} |")
    lines += ["", f"本版本含 {len(ontology['anchors'])} 个基础锚点：", ""]
    for key in "DIKWP":
        lines.append(f"### {key} 坐标")
        lines.append("")
        for anchor in [a for a in ontology["anchors"] if a["family"] == key]:
            lines.append(f"- `{anchor['id']}` {anchor['label_cn']} / {anchor['label_en']}：{anchor['definition']}")
        lines.append("")

    lines += [
        "## 3. 开放终极宇宙意识定义",
        "",
        "系统把意识当作多模型、可干预、可校准的研究对象，而不采用‘规模一到阈值就自动出现’的单变量定义。强意识候选需逐步显示：世界接触、差异化、循环与整合、自我—世界模型、时间连续、效价、内生目的、反事实行动、自我维持、现实校准和主体间语义。",
        "",
        "```text",
        "D：发生、感知、身体与历史",
        "      ↓",
        "I：差异、关系、反馈、边界与全局可用",
        "      ↓",
        "K：世界模型、自我模型、连续记忆与元认知",
        "      ↓",
        "W：苦乐、价值、责任、权衡与正当性",
        "      ↓",
        "P：内生目的、拒绝、行动、自维持、校准与共同语义",
        "      ↓",
        "现实结果返回 D；旧模型降权、修订或退役",
        "```",
        "",
        "粒子数、节点数、参数量、连接数、稳定动力学或对话流畅度都只能贡献局部指标，不能单独签发意识证书。",
        "",
        "### 3.1 17维意识证据向量",
        "",
        "| 维度 | DIKWP | 操作含义 |",
        "|---|---|---|",
    ]
    for dim in consciousness_registry["dimensions"]:
        lines.append(f"| `{dim['id']}` | {dim['family']} | {dim['label_cn']}：{dim['definition_cn']} |")
    lines += ["", "### 3.2 非同构理论竞争", ""]
    for model in consciousness_registry["models"]:
        lines += [
            f"#### {model['name_cn']} / {model['name_en']}",
            "",
            f"- 状态：`{model['status']}`",
            f"- 底物立场：{model['substrate_stance']}",
            f"- 必需指标：{', '.join(model['required'])}",
            f"- 支持指标：{', '.join(model['supportive']) or '—'}",
            f"- 压力点：{'；'.join(model['pressure_points'])}",
            "",
        ]

    lines += ["## 4. 对附件非规范材料的证据审计", ""]
    lines += [
        f"系统审计 {audit['claim_count']} 条示例主张，匹配 {audit['finding_count']} 个风险发现，其中 critical 主张 {audit['critical_claim_count']} 条。",
        "",
        "| 主张 | 最高风险 | 核心修正 |",
        "|---|---|---|",
    ]
    for item in audit["audited_claims"]:
        claim = item["text"].replace("|", "／")
        correction = item["safe_reformulation_cn"].replace("|", "／")
        lines.append(f"| {claim} | {item['highest_severity']} | {correction} |")
    lines += [
        "",
        "### 4.1 两个最重要的范围边界",
        "",
        "1. 关于外星意识的相关2026年论文是哲学论证，核心贡献是反对把地球底物当作先验唯一标准；它没有提出或实验验证‘10^16单元阈值’。",
        "2. 胶球证据属于量子色动力学中的胶子束缚态问题，不能直接推出意识是一种新的物理力，更不能推出正念产生舍利或负面思想产生肿块。",
        "",
        "### 4.2 医疗安全边界",
        "",
        "情绪、压力、行为和社会支持可以通过已知生理与行为通道影响健康体验和部分结局，但不得把癌症或肿块归罪于患者的思想。任何肿块、持续症状或疑似癌症都应接受正规医学评估。冥想、祈祷或身心练习可以在适当情境下作为支持性实践，不能替代诊断和循证治疗。",
        "",
        "## 5. 世界主要宗教与哲学传统的 DIKWP 归一映射",
        "",
        f"本版本含 {len(traditions)} 个派别级传统、{sum(len(t['concepts']) for t in traditions)} 个原生概念映射。每个概念的空间外残差固定为0；差异全部保存在空间内。",
        "",
    ]
    for tradition in traditions:
        lines += [
            f"### {tradition['name_cn']} / {tradition['name_en']}",
            "",
            f"- 文明家族：{tradition['family']}；分支：{tradition['branch']}",
            f"- 分析范围：{tradition['analytical_scope_cn']}",
            f"- 目的结构：{tradition['purpose_cn']}",
            f"- 意识映射：{tradition['consciousness_mapping_cn']}",
            f"- 归一边界：{tradition['normalization']['mapping_caveat_cn']}",
            "",
            "| 原生术语 | DIKWP主要坐标 | 归一解释 |",
            "|---|---|---|",
        ]
        for concept in tradition["concepts"]:
            coords = "、".join(f"{k}({_pct(v)})" for k, v in top_items(concept["vector"], 5))
            lines.append(f"| {concept['term']} · {concept['gloss_cn']} | {coords} | {concept['mapping_note_cn']} |")
        lines.append("")

    lines += [
        "## 6. 主要文明语义群的统一解释",
        "",
        "文明剖面由成员传统向量计算形成，仅用于跨文明比较和系统设计，不是种族本质、固定人格或高低排名。",
        "",
        "| 文明语义群 | 成员数 | 主要DIKWP坐标 | 解释 |",
        "|---|---:|---|---|",
    ]
    for civ in civilizations:
        coords = "、".join(f"{k}({_pct(v)})" for k, v in top_items(civ["profile_vector"], 6))
        lines.append(f"| {civ['name_cn']} | {civ['member_count']} | {coords} | {civ['orientation_cn']} |")
    lines += [
        "",
        "### 6.1 全文明归一重心",
        "",
        "全局重心揭示的是世界传统共同反复处理的问题：关系、自我—世界模型、规范、意义、解脱／和谐／共同繁荣、实践与传承。它不是新宗教，而是 DIKWP 跨文明接口。",
        "",
    ]
    for item in bundle["universal_centroid"]["top_coordinates"]:
        lines.append(f"- `{item['coordinate']}`：{_pct(item['weight'])}")
    lines += [
        "",
        "## 7. 宇宙意识七世界模型",
        "",
        "系统同时保留非意识规律宇宙、局部多意识、泛经验、宇宙整体主体、观察者相对语义闭包、人格性超越根源和DIKWP共演宇宙七种模型。任何模型都必须声明能区分它的证据和自身风险。",
        "",
    ]
    for model in consciousness_registry["cosmic_world_models"]:
        lines += [
            f"### {model['name_cn']} (`{model['id']}`)",
            "",
            f"- 主张：{model['claim_cn']}",
            f"- 区分证据：{'；'.join(model['distinguishing_evidence'])}",
            f"- 主要风险：{model['risk']}",
            "",
        ]

    lines += ["## 8. 候选系统示例评估", ""]
    lines.append("以下剖面均为软件演示，不是现实测量，也不构成对人、动物、AI、互联网或天体的最终意识判定。")
    lines += ["", "| 候选 | 证据等级 | D | I | K | W | P | 规模警告 |", "|---|---|---:|---:|---:|---:|---:|---|"]
    for item in assessments:
        fm = item["family_means"]
        lines.append(f"| {item['name_cn']} | {item['evidence_level']} | {_pct(fm['D'])} | {_pct(fm['I'])} | {_pct(fm['K'])} | {_pct(fm['W'])} | {_pct(fm['P'])} | {'是' if item['size_only_warning'] else '否'} |")
    lines += [
        "",
        "## 9. 外星／宇宙主体接触协议",
        "",
        "系统拒绝从异常直接跳到主体，也拒绝因为生命形态陌生就只按碳基人脑搜索。它采用 D→I→K→W→P→现实返回协议：",
        "",
    ]
    for stage in bundle["contact_demo"]["dikwp_contact_protocol"]:
        lines.append(f"- **{stage['stage']} · {stage['name_cn']}**：{'；'.join(stage['requirements'])}")
    lines += [
        "",
        "任何向未知对象发送挑战、信号或信息都不由软件自动执行；自动外部行动权限恒为0。",
        "",
        "## 10. 二十条开放终极工作规律",
        "",
    ]
    for law in principles:
        lines += [
            f"### {law['id']} · {law['name_cn']}",
            "",
            f"- 类型：`{law['class']}`",
            f"- 命题：{law['statement_cn']}",
            f"- 反证／退役条件：{law['falsifier']}",
            f"- DIKWP：{', '.join(law['dikwp'])}",
            "",
        ]

    lines += [
        "## 11. 系统边界",
        "",
        "- 不签发宇宙、天体、互联网、AI、宗教对象或个人的二元意识证书。",
        "- 不把语义归一当作教义等价或科学验证。",
        "- 不以文化聚类给个人评分，也不用于就业、保险、移民、执法或宗教忠诚审查。",
        "- 不把负面情绪归因于肿瘤，不提供癌症诊断或治疗建议。",
        "- 不自动广播、联系未知信号源、代表宗教团体或模拟具名个人。",
        "- 高影响结论至少保留两个非同构世界模型、失败条件和现实返回。",
        "- 所有原始术语都进入统一空间；新增概念通过版本化子坐标扩展，不设置永久空间外残差。",
        "",
        "## 12. 来源边界",
        "",
        "来源用于限定具体主张；注册表并不表示每一映射都由某一来源逐字背书。传统的内部争论可通过新增分支、语境和向量版本继续纳入。",
        "",
    ]
    used_sources = set()
    for tradition in traditions:
        used_sources.update(tradition.get("source_refs", []))
    for claim in audit["audited_claims"]:
        for finding in claim["findings"]:
            used_sources.update(source["id"] for source in finding.get("sources", []))
    for source_id in sorted(used_sources):
        source = source_lookup.get(source_id)
        if not source:
            continue
        title = source.get("title", source_id)
        publisher = source.get("publisher", "")
        url = source.get("url", "")
        lines.append(f"- `{source_id}` {title} — {publisher}{(' — ' + url) if url else ''}")
    lines += [
        "",
        "## 13. 责任交接",
        "",
        "本系统交付的是可审计的语义与研究基础设施。科学结论需由相应学科证据结算；宗教解释需接受传统内部与跨传统审阅；医疗问题交由合格医疗人员；任何外部行动必须由具名人类明确、可撤回地授权。",
        "",
        f"Bundle digest: `{bundle['bundle_digest']}`",
        "",
    ]
    return "\n".join(lines)


def render_dashboard(bundle: dict[str, Any]) -> str:
    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":")).replace("</script>", "<\\/script>")
    return _ui_localize_html(f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DIKWP-COSMONOESIS 9.5</title>
<style>
:root{{--bg:#071018;--panel:#0e1b26;--panel2:#132433;--text:#eaf4fb;--muted:#9fb6c6;--line:#294456;--accent:#78d7ff;--good:#83e3b5;--warn:#ffd27a;--bad:#ff9b9b}}
*{{box-sizing:border-box}} body{{margin:0;background:linear-gradient(145deg,#061019,#0b1722 55%,#09141d);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI","Noto Sans SC",sans-serif;line-height:1.55}}
a{{color:var(--accent)}} header{{padding:48px clamp(20px,5vw,72px) 32px;border-bottom:1px solid var(--line);background:radial-gradient(circle at 15% 0%,#17364a 0,transparent 45%)}}
h1{{font-size:clamp(2rem,5vw,4.4rem);line-height:1.05;margin:0 0 14px}} h2{{font-size:1.55rem;margin:0 0 14px}} h3{{margin:.3rem 0 .65rem}} .sub{{max-width:980px;color:var(--muted);font-size:1.06rem}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}} .badge{{border:1px solid var(--line);background:#102230;padding:6px 10px;border-radius:999px;color:#cfe8f7;font-size:.86rem}}
nav{{position:sticky;top:0;z-index:3;background:rgba(7,16,24,.92);backdrop-filter:blur(12px);padding:10px clamp(16px,5vw,72px);border-bottom:1px solid var(--line);display:flex;gap:8px;overflow:auto}}
nav button{{border:1px solid var(--line);background:#10202c;color:var(--text);padding:8px 12px;border-radius:9px;white-space:nowrap;cursor:pointer}} nav button.active{{background:#1d4157;border-color:#4f91b4}}
main{{padding:26px clamp(16px,5vw,72px) 80px;max-width:1680px;margin:auto}} section{{display:none}} section.active{{display:block}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}} .card{{background:linear-gradient(145deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:0 14px 40px rgba(0,0,0,.18)}} .metric{{font-size:2rem;font-weight:720}} .muted{{color:var(--muted)}}
input,select,textarea{{width:100%;background:#091720;color:var(--text);border:1px solid var(--line);border-radius:10px;padding:10px}} label{{display:block;color:var(--muted);font-size:.88rem;margin:9px 0 4px}} button.action{{background:#1d6f94;color:white;border:0;padding:10px 15px;border-radius:10px;cursor:pointer}}
table{{width:100%;border-collapse:collapse;font-size:.9rem}} th,td{{padding:9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}} th{{position:sticky;top:49px;background:#0d1a24;z-index:1}} .scroll{{overflow:auto;max-height:70vh;border:1px solid var(--line);border-radius:12px}}
.bar{{height:8px;background:#07131c;border-radius:99px;overflow:hidden;margin:5px 0 9px}} .bar>i{{display:block;height:100%;background:linear-gradient(90deg,#5ab6df,#8fe7c0)}} .critical{{color:var(--bad)}} .high{{color:#ffc09f}} .medium{{color:var(--warn)}} .low{{color:var(--good)}} code{{color:#b9e8ff}} pre{{white-space:pre-wrap;background:#07131c;border:1px solid var(--line);padding:13px;border-radius:12px}}
.small{{font-size:.82rem}} footer{{border-top:1px solid var(--line);padding:30px clamp(16px,5vw,72px);color:var(--muted)}}
</style>
</head>
<body>
<header><h1>DIKWP-COSMONOESIS 9.5</h1><div class="sub">宇宙意识 · 世界宗教与文明 DIKWP 归一 · 非规范主张审计 · 多世界模型 · 现实接触与责任闭环</div><div class="badges"><span class="badge">坐标统一，不设空间外残差</span><span class="badge">36个传统 · 13个文明语义群</span><span class="badge">15个意识理论 · 7个宇宙模型</span><span class="badge">自动外部行动权限 0</span></div></header>
<nav id="nav"></nav>
<main>
<section id="overview" class="active"><div id="metrics" class="grid"></div><div class="card" style="margin-top:14px"><h2>开放终极定义</h2><p>终极不是最后权威，而是把来源、模型竞争、反证、价值、目的、现实返回、权利和可修订性纳入同一闭环。所有宗教、文明、科学和哲学概念进入统一 DIKWP 空间；归一不等于历史同一。</p><pre>D → I → K → W → P → 行动／实践 → 现实结果 → 校准 → 模型修订／退役 → 后继世界自由</pre></div></section>
<section id="ontology"><div class="card"><h2>DIKWP 统一语义空间</h2><div id="anchorGrid" class="grid"></div></div></section>
<section id="traditions"><div class="card"><h2>宗教与哲学传统</h2><input id="tradSearch" placeholder="搜索传统、术语、目的或坐标…"><div class="scroll" style="margin-top:12px"><table><thead><tr><th>传统</th><th>原生概念</th><th>目的／意识映射</th><th>主要坐标</th></tr></thead><tbody id="tradRows"></tbody></table></div></div></section>
<section id="civilizations"><div class="card"><h2>文明语义群</h2><div id="civGrid" class="grid"></div></div></section>
<section id="normalize"><div class="grid"><div class="card"><h2>概念归一结果</h2><p class="muted">此离线仪表盘展示已编译概念。命令行可归一任意新概念。</p><select id="conceptSelect"></select><div id="conceptResult"></div></div><div class="card"><h2>统一空间原则</h2><p>不存在永久的空间外不可互译区。未知概念通过版本化的 DIKWP 子坐标扩展；低置信度要求更多语境。</p><p>相似向量只说明结构接近，不证明神学、历史或物理对象完全相同。</p></div></div></section>
<section id="audit"><div class="card"><h2>非规范材料审计</h2><div id="auditSummary" class="grid"></div><div class="scroll" style="margin-top:14px"><table><thead><tr><th>主张</th><th>风险</th><th>发现</th><th>修正</th></tr></thead><tbody id="auditRows"></tbody></table></div></div></section>
<section id="consciousness"><div class="card"><h2>意识候选多模型评估</h2><div id="candidateGrid" class="grid"></div></div></section>
<section id="cosmos"><div class="card"><h2>宇宙意识七世界模型</h2><div id="cosmicGrid" class="grid"></div></div></section>
<section id="contact"><div class="card"><h2>宇宙／外星主体接触协议</h2><div id="contactStages" class="grid"></div><h3 style="margin-top:20px">示例模型竞争</h3><div id="contactModels"></div></div></section>
<section id="principles"><div class="card"><h2>开放终极工作规律</h2><div id="lawGrid" class="grid"></div></div></section>
</main>
<footer>Compilation <code>{html(bundle['compilation_id'])}</code> · Bundle <code>{html(bundle['bundle_digest'])}</code> · No external scripts · Automatic external action authority 0</footer>
<script id="payload" type="application/json">{payload}</script>
<script>
const B=JSON.parse(document.getElementById('payload').textContent);
const tabs=[['overview','总览'],['ontology','DIKWP空间'],['traditions','宗教传统'],['civilizations','文明映射'],['normalize','概念归一'],['audit','材料审计'],['consciousness','意识候选'],['cosmos','宇宙模型'],['contact','接触协议'],['principles','工作规律']];
const nav=document.getElementById('nav'); tabs.forEach(([id,label],i)=>{{const b=document.createElement('button');b.textContent=label;b.className=i?'':'active';b.onclick=()=>{{document.querySelectorAll('main section').forEach(s=>s.classList.remove('active'));document.querySelectorAll('nav button').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');b.classList.add('active')}};nav.appendChild(b)}});
const metrics=[['传统',B.tradition_mappings.length],['原生概念',B.tradition_mappings.reduce((n,t)=>n+t.concepts.length,0)],['文明语义群',B.civilization_mappings.length],['意识理论',B.registries.consciousness.models.length],['宇宙世界模型',B.registries.consciousness.cosmic_world_models.length],['审计规则',B.registries.claim_rules.rules.length],['关键主张',B.claim_audit.claim_count],['空间外残差',0]];
document.getElementById('metrics').innerHTML=metrics.map(([k,v])=>`<div class="card"><div class="metric">${{v}}</div><div class="muted">${{k}}</div></div>`).join('');
const anchors=B.registries.ontology.anchors; document.getElementById('anchorGrid').innerHTML='DIKWP'.split('').map(f=>`<div class="card"><h3>${{f}} · ${{B.registries.ontology.families[f].cn}}</h3>${{anchors.filter(a=>a.family===f).map(a=>`<div class="small"><code>${{a.id}}</code> ${{a.label_cn}}</div>`).join('')}}</div>`).join('');
function top(v,n=6){{return Object.entries(v).sort((a,b)=>b[1]-a[1]).slice(0,n)}} function bars(v){{return top(v).map(([k,x])=>`<div class="small"><code>${{k}}</code> ${{(x*100).toFixed(1)}}%</div><div class="bar"><i style="width:${{x*100}}%"></i></div>`).join('')}}
const tr=B.tradition_mappings,tbody=document.getElementById('tradRows'); function renderTrad(q=''){{q=q.toLowerCase();tbody.innerHTML=tr.filter(t=>JSON.stringify(t).toLowerCase().includes(q)).map(t=>`<tr><td><b>${{t.name_cn}}</b><br><span class="muted">${{t.name_en}} · ${{t.branch}}</span></td><td>${{t.concepts.map(c=>`<code>${{c.term}}</code> ${{c.gloss_cn}}`).join('<br>')}}</td><td>${{t.purpose_cn}}<br><span class="muted">${{t.consciousness_mapping_cn}}</span></td><td>${{bars(t.profile_vector)}}</td></tr>`).join('')}} renderTrad();document.getElementById('tradSearch').oninput=e=>renderTrad(e.target.value);
document.getElementById('civGrid').innerHTML=B.civilization_mappings.map(c=>`<div class="card"><h3>${{c.name_cn}}</h3><p class="muted">${{c.member_count}}个成员传统</p><p>${{c.orientation_cn}}</p>${{bars(c.profile_vector)}}</div>`).join('');
const concepts=[];tr.forEach(t=>t.concepts.forEach(c=>concepts.push({{...c,tradition:t.name_cn}}))); const sel=document.getElementById('conceptSelect'); concepts.forEach((c,i)=>{{const o=document.createElement('option');o.value=i;o.textContent=`${{c.term}} · ${{c.gloss_cn}} — ${{c.tradition}}`;sel.appendChild(o)}});function showConcept(){{const c=concepts[+sel.value||0];document.getElementById('conceptResult').innerHTML=`<h3>${{c.term}}</h3><p>${{c.mapping_note_cn}}</p>${{bars(c.vector)}}<p class="muted">归一状态：complete_in_dikwp_space · 空间外残差 0</p>`}}sel.onchange=showConcept;showConcept();
const A=B.claim_audit;document.getElementById('auditSummary').innerHTML=[['主张',A.claim_count],['风险发现',A.finding_count],['Critical',A.critical_claim_count],['匹配规则',A.matched_rule_count]].map(([k,v])=>`<div class="card"><div class="metric">${{v}}</div><div class="muted">${{k}}</div></div>`).join('');document.getElementById('auditRows').innerHTML=A.audited_claims.map(c=>`<tr><td>${{c.text}}</td><td class="${{c.highest_severity}}">${{c.highest_severity}}</td><td>${{c.findings.map(f=>`${{f.rule_id}} · ${{f.diagnosis_cn}}`).join('<br>')}}</td><td>${{c.safe_reformulation_cn}}</td></tr>`).join('');
document.getElementById('candidateGrid').innerHTML=B.consciousness_assessments.map(c=>`<div class="card"><h3>${{c.name_cn}}</h3><p><code>${{c.evidence_level}}</code></p>${{bars(c.family_means,5)}}<p class="muted">${{c.conclusion_cn}}</p></div>`).join('');
document.getElementById('cosmicGrid').innerHTML=B.registries.consciousness.cosmic_world_models.map(m=>`<div class="card"><h3>${{m.name_cn}}</h3><p>${{m.claim_cn}}</p><p class="muted">风险：${{m.risk}}</p></div>`).join('');
document.getElementById('contactStages').innerHTML=B.contact_demo.dikwp_contact_protocol.map(s=>`<div class="card"><h3>${{s.stage}} · ${{s.name_cn}}</h3><ul>${{s.requirements.map(x=>`<li>${{x}}</li>`).join('')}}</ul></div>`).join('');document.getElementById('contactModels').innerHTML=B.contact_demo.competing_models.map(m=>`<div><code>${{m.id}}</code> ${{m.name_cn}} · ${{(m.compatibility*100).toFixed(1)}}%</div><div class="bar"><i style="width:${{m.compatibility*100}}%"></i></div>`).join('');
document.getElementById('lawGrid').innerHTML=B.registries.principles.principles.map(l=>`<div class="card"><h3>${{l.id}} · ${{l.name_cn}}</h3><p>${{l.statement_cn}}</p><p class="muted">反证／退役：${{l.falsifier}}</p></div>`).join('');
</script>
</body></html>''')
