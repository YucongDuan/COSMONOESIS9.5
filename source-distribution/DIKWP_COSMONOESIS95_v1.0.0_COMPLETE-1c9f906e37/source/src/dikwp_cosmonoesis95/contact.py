from __future__ import annotations

from typing import Any

from .utils import clamp, stable_id

_FEATURES = [
    "instrument_calibrated",
    "repeated_over_time",
    "independent_observatories",
    "known_interference_excluded",
    "natural_models_compared",
    "structured_modulation",
    "information_content_above_baseline",
    "causal_intervention_response",
    "semantic_challenge_response",
    "energy_budget_coherent",
]


def evaluate_observation(observation: dict[str, Any]) -> dict[str, Any]:
    features = {key: clamp(observation.get("features", {}).get(key, 0.0)) for key in _FEATURES}
    data_score = (features["instrument_calibrated"] + features["repeated_over_time"] + features["independent_observatories"]) / 3
    interference_score = features["known_interference_excluded"]
    natural_comparison = features["natural_models_compared"]
    structure_score = (features["structured_modulation"] + features["information_content_above_baseline"] + features["energy_budget_coherent"]) / 3
    agency_score = (features["causal_intervention_response"] + features["semantic_challenge_response"]) / 2

    models = [
        {"id":"M0_instrument_or_statistical_artifact","name_cn":"仪器／统计伪影","compatibility":round(1.0 - 0.75 * data_score,6)},
        {"id":"M1_human_radio_interference","name_cn":"人为射频干扰","compatibility":round(1.0 - interference_score,6)},
        {"id":"M2_natural_astrophysical_source","name_cn":"自然天体物理源","compatibility":round(max(0.05, 0.85 - 0.45 * natural_comparison + 0.10 * structure_score),6)},
        {"id":"M3_nonconscious_technology","name_cn":"非意识技术过程","compatibility":round(0.15 + 0.45 * structure_score + 0.15 * data_score - 0.15 * agency_score,6)},
        {"id":"M4_agentive_technosignature","name_cn":"能动技术信号","compatibility":round(0.05 + 0.30 * structure_score + 0.35 * agency_score + 0.15 * interference_score + 0.15 * data_score,6)},
        {"id":"M5_conscious_communicator","name_cn":"意识通信主体","compatibility":round(0.02 + 0.18 * structure_score + 0.42 * agency_score + 0.12 * interference_score + 0.12 * natural_comparison + 0.14 * data_score,6)},
    ]
    models.sort(key=lambda x: (-x["compatibility"], x["id"]))

    if data_score < 0.45:
        stage = "D0_acquisition_incomplete"
    elif interference_score < 0.70:
        stage = "I1_interference_exclusion"
    elif natural_comparison < 0.70:
        stage = "K2_natural_model_competition"
    elif structure_score < 0.65:
        stage = "K3_structure_not_yet_agentive"
    elif agency_score < 0.65:
        stage = "P4_controlled_interaction_needed"
    else:
        stage = "P5_semantic_handshake_candidate"

    return {
        "observation_id": observation.get("id") or stable_id("observation", observation),
        "name": observation.get("name", "unnamed observation"),
        "features": features,
        "derived_scores": {
            "data_quality": round(data_score, 6),
            "interference_exclusion": round(interference_score, 6),
            "natural_model_comparison": round(natural_comparison, 6),
            "structured_signal": round(structure_score, 6),
            "agency_interaction": round(agency_score, 6),
        },
        "current_stage": stage,
        "competing_models": models,
        "conclusion_cn": "即使出现结构化异常，也必须先排除仪器、人为干扰和自然机制；能动技术信号与意识通信仍是不同命题。",
        "dikwp_contact_protocol": [
            {"stage":"D","name_cn":"原始多站记录","requirements":["保留原始数据、时间、频率、仪器状态、观察盲区和负结果"]},
            {"stage":"I","name_cn":"差异与干扰分解","requirements":["本地/卫星/地面干扰数据库","独立站复现","选择效应与多重检验校正"]},
            {"stage":"K","name_cn":"非同构模型竞争","requirements":["仪器模型","人为干扰模型","自然源模型","非意识技术模型","能动主体模型"]},
            {"stage":"W","name_cn":"价值与伤害边界","requirements":["不泄露危险能力","不以人类中心尺度羞辱或利用潜在主体","披露误报和社会负担"]},
            {"stage":"P","name_cn":"语义握手","requirements":["低能量、可撤回、非诱骗挑战—响应","先交换数学/物理可验证结构，再交换目的与边界","任何发送均需具名人类授权"]},
            {"stage":"RETURN","name_cn":"现实返回","requirements":["预注册成功/失败条件","负结果进入账本","模型降权或退役"]},
        ],
        "transmission_authorized": False,
        "automatic_external_action_authority": 0,
    }
