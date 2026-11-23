"""
Lifecycle Public Health AI Ethics Scorecard.
Harmonizes:
- WHO (2021): Ethics and Governance of AI for Health (6 core principles)
- ICMR (2023): Ethical Guidelines for Application of AI in Biomedical Research and Healthcare
- FUTURE-AI (Lekadir et al., 2021): Fairness, Universality, Traceability, Usability, Robustness, Explainability
- Floridi et al. (2018): AI4People Framework
"""

from typing import Dict, Any, List

LIFECYCLE_STAGES = {
    "stage_1": {
        "title": "Stage 1: Problem Formulation & Epistemic Justification",
        "description": "Validates whether AI is ethically appropriate, necessary, and designed with affected communities.",
        "guideline_sources": "WHO (2021) Principle 1 & 4; ICMR (2023) Section 2; Floridi et al. (2018) Beneficence.",
        "metrics": [
            {
                "id": "p1_clinical_need",
                "label": "Genuine Public Health Necessity & Proportionality",
                "help": "Does the system address a documented, urgent public health priority that cannot be solved by simpler non-AI methods?",
                "weight": 1.0
            },
            {
                "id": "p2_alternative_comparison",
                "label": "Benchmarking Against Simpler Alternatives",
                "help": "Has the AI been compared rigorously against standard clinical heuristics, simple regression, or conventional triage?",
                "weight": 1.0
            },
            {
                "id": "p3_stakeholder_engagement",
                "label": "Participatory Design with Vulnerable Communities",
                "help": "Were marginalized groups, patient advocates, and front-line healthcare workers actively involved in problem framing?",
                "weight": 1.2
            },
            {
                "id": "p4_intended_context",
                "label": "Contextual Scope & Environmental Feasibility",
                "help": "Is the system tailored to the operational realities (power, connectivity, staffing) of the target health facilities?",
                "weight": 0.8
            },
            {
                "id": "p5_deontological_limits",
                "label": "Red-Line Definition & Non-Negotiable Human Rights",
                "help": "Are there explicit ethical boundaries preventing autonomous life-or-death decisions without human physician override?",
                "weight": 1.2
            }
        ]
    },

    "stage_2": {
        "title": "Stage 2: Data Provenance, Representativeness & Privacy",
        "description": "Audits the training and testing datasets for historical bias, missingness, and consent hygiene.",
        "guideline_sources": "ICMR (2023) Section 3; FUTURE-AI (Universality); WHO Principle 2 (Fostering Safety and Wellbeing).",
        "metrics": [
            {
                "id": "d1_demographic_parity",
                "label": "Demographic & Geographic Dataset Diversity",
                "help": "Does the training cohort represent underprivileged castes, rural districts, elderly cohorts, and gender balances?",
                "weight": 1.3
            },
            {
                "id": "d2_label_fidelity",
                "label": "Gold-Standard Ground Truth vs. Biased Proxy Labels",
                "help": "Are outcome labels based on true pathology (e.g. molecular test) rather than biased proxies like healthcare expenditure?",
                "weight": 1.2
            },
            {
                "id": "d3_temporal_shift",
                "label": "Temporal Robustness & Mutation/Strain Shift",
                "help": "Has the data been tested against epidemiological shifts (e.g., new viral variants, changing treatment guidelines)?",
                "weight": 1.0
            },
            {
                "id": "d4_missingness_bias",
                "label": "Systematic Data Missingness Audit",
                "help": "Does the model explicitly handle missing clinical tests without penalizing poor patients who lack diagnostic lab access?",
                "weight": 1.0
            },
            {
                "id": "d5_data_privacy",
                "label": "Differential Privacy & Informed Institutional Consent",
                "help": "Are strict cryptographic safeguards, de-identification, and ICMR-compliant ethics board approvals in place?",
                "weight": 1.0
            }
        ]
    },

    "stage_3": {
        "title": "Stage 3: Algorithmic Optimization & Distributive Fairness",
        "description": "Evaluates mathematical objective functions for distributive justice, explainability, and uncertainty.",
        "guideline_sources": "WHO Principle 3 (Ensuring Equity and Non-discrimination); Kleinberg et al. (2016); FUTURE-AI.",
        "metrics": [
            {
                "id": "a1_fairness_metric",
                "label": "Formal Mathematical Fairness Constraints",
                "help": "Does the model optimization enforce equalized odds, predictive parity, or Rawlsian maximin constraints across subgroups?",
                "weight": 1.3
            },
            {
                "id": "a2_explainability",
                "label": "Clinically Interpretable Explanations",
                "help": "Does the algorithm provide actionable, biologically plausible explanations (e.g., saliency maps, SHAP) to clinicians?",
                "weight": 1.0
            },
            {
                "id": "a3_calibration",
                "label": "Multi-Subgroup Risk Calibration",
                "help": "Is a predicted 30% risk of mortality equally accurate for elderly patients as it is for younger cohorts?",
                "weight": 1.1
            },
            {
                "id": "a4_epistemic_uncertainty",
                "label": "Confidence Scoring & Epistemic Uncertainty Quantification",
                "help": "Does the system express 'I do not know' when encountering out-of-distribution demographic or pathological patterns?",
                "weight": 1.0
            },
            {
                "id": "a5_human_in_loop",
                "label": "Human Agency & Meaningful Clinical Oversight",
                "help": "Can clinicians easily challenge, override, or disregard the algorithm without administrative friction?",
                "weight": 1.2
            }
        ]
    },

    "stage_4": {
        "title": "Stage 4: Post-Market Governance, Contestability & Drift",
        "description": "Continuous monitoring of algorithmic drift, real-world adverse outcomes, and institutional accountability.",
        "guideline_sources": "WHO Principle 5 & 6 (Sustainability & Accountability); ICMR Section 5; FUTURE-AI (Traceability).",
        "metrics": [
            {
                "id": "g1_continuous_drift_audit",
                "label": "Continuous Performance & Fairness Drift Monitoring",
                "help": "Is there a real-time dashboard tracking accuracy degradation, demographic shifts, and alert frequency post-launch?",
                "weight": 1.2
            },
            {
                "id": "g2_contestability_override",
                "label": "Patient & Provider Contestability Mechanism",
                "help": "Is there an established institutional grievance mechanism for patients denied care due to an algorithmic score?",
                "weight": 1.2
            },
            {
                "id": "g3_alert_fatigue_mitigation",
                "label": "Alert Fatigue & Usability Ergonomics",
                "help": "Is positive predictive value high enough to prevent clinical desensitization and workflow burnout?",
                "weight": 0.9
            },
            {
                "id": "g4_vendor_liability",
                "label": "Clear Legal Liability & Vendor Responsibility",
                "help": "Do contracts clearly delineate legal liability between the software vendor, hospital administration, and clinicians?",
                "weight": 1.1
            },
            {
                "id": "g5_public_transparency",
                "label": "Algorithmic Transparency & Open Registry Listing",
                "help": "Is the algorithm registered in public trial registries (e.g. CTRI, clinicaltrials.gov) with open audit protocols?",
                "weight": 1.0
            }
        ]
    }
}


def calculate_lifecycle_scores(user_scores: Dict[str, float]) -> Dict[str, Any]:
    """
    Computes weighted stage scores and overall ethical compliance tier.
    Each metric is scored from 1.0 (severe deficiency) to 5.0 (gold-standard ethical compliance).
    """
    stage_results = {}
    total_weighted_points = 0.0
    total_possible_points = 0.0

    for stage_key, stage_info in LIFECYCLE_STAGES.items():
        stage_pts = 0.0
        stage_max = 0.0
        for m in stage_info["metrics"]:
            m_id = m["id"]
            score = user_scores.get(m_id, 3.0)
            weight = m["weight"]
            stage_pts += score * weight
            stage_max += 5.0 * weight

        pct = (stage_pts / stage_max) * 100.0
        stage_results[stage_key] = {
            "title": stage_info["title"],
            "score": round(stage_pts, 2),
            "max": round(stage_max, 2),
            "percentage": round(pct, 1)
        }
        total_weighted_points += stage_pts
        total_possible_points += stage_max

    overall_pct = (total_weighted_points / total_possible_points) * 100.0

    if overall_pct >= 80.0:
        tier = "Ethically Robust (Low Risk)"
        tier_color = "#10B981" # Green
        recommendation = "System meets high standards across WHO and ICMR guidelines. Safe for phased clinical pilot."
    elif overall_pct >= 60.0:
        tier = "Conditional Approval (Moderate Ethical Risk)"
        tier_color = "#F59E0B" # Amber
        recommendation = "Notable gaps in subgroup fairness, contestability, or data provenance. Requires mitigation before deployment."
    else:
        tier = "High Ethical Risk (Deployment Halted)"
        tier_color = "#EF4444" # Red
        recommendation = "Critical violations of non-discrimination, transparency, or human agency. Significant harm potential."

    return {
        "overall_percentage": round(overall_pct, 1),
        "overall_score": round(total_weighted_points, 1),
        "max_score": round(total_possible_points, 1),
        "ethical_tier": tier,
        "tier_color": tier_color,
        "recommendation": recommendation,
        "stages": stage_results
    }
