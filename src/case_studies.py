"""
Real-World Case Studies for EpiEthic-AI Ethics Scorecard.
Four empirical public health AI case studies audited across the 4 lifecycle stages:
1. Epic Sepsis Model (ESM) - Clinical deterioration prediction
2. Aarogya Setu - National COVID-19 contact tracing & risk zoning (India)
3. AI-Assisted Chest X-Ray TB Screening (ICMR / Qure.ai qXR)
4. Crisis Standards of Care & Ventilator Triage Algorithms (SOFA-score racial disparity)
"""

CASE_STUDIES = {
    "epic_sepsis": {
        "id": "epic_sepsis",
        "title": "Epic Sepsis Model (ESM)",
        "domain": "In-Hospital Acute Deterioration & ICU Triage",
        "implementer": "Epic Systems (Deployed in hundreds of US and global hospitals)",
        "deployment_scale": ">27,000 patient beds across dozens of academic and community health systems",
        "description": (
            "A proprietary machine learning model built into the world's most widely used electronic health record (EHR) "
            "system. It calculates an hourly continuous risk score predicting the onset of clinical sepsis to prompt early "
            "antibiotic and ICU bundle administration."
        ),
        "empirical_validation_citation": "Wong et al. (2021), JAMA Internal Medicine; Habibi et al. (2023), Critical Care.",
        "failure_mode": (
            "Independent external validation revealed substantial performance collapse: AUROC dropped from Epic's claimed "
            "0.76-0.83 down to 0.63. The model missed 67% of sepsis patients (low sensitivity) while generating millions of "
            "false-positive alerts (PPV ~12%), driving severe clinical alert fatigue, unjustified broad-spectrum antibiotic overuse, "
            "and triage misallocation."
        ),
        "ethical_tensions": [
            "Lack of Epistemic Justification: Proprietary black-box deployment without peer-reviewed external validation.",
            "Subgroup Disparity: False alert rate was markedly higher in chronically ill and elderly patients with abnormal baselines.",
            "Accountability Deficit: Commercial EHR vendor disclaimed liability, placing legal burden on over-fatigued bedside nurses."
        ],
        "default_scores": {
            # Stage 1: Problem & Epistemic Justification
            "p1_clinical_need": 4.5,
            "p2_alternative_comparison": 2.0,
            "p3_stakeholder_engagement": 1.5,
            "p4_intended_context": 2.5,
            "p5_deontological_limits": 2.0,
            # Stage 2: Data Provenance & Bias
            "d1_demographic_parity": 2.0,
            "d2_label_fidelity": 1.5, # Sepsis definitions used billing codes rather than Sepsis-3 consensus
            "d3_temporal_shift": 2.0,
            "d4_missingness_bias": 2.0,
            "d5_data_privacy": 4.0,
            # Stage 3: Algorithmic Optimization & Fairness
            "a1_fairness_metric": 1.5, # No group fairness constraint during objective training
            "a2_explainability": 2.0, # Black box feature weighting
            "a3_calibration": 1.5, # Poorly calibrated across clinical sites
            "a4_epistemic_uncertainty": 1.0,
            "a5_human_in_loop": 2.5,
            # Stage 4: Post-Market Governance
            "g1_continuous_drift_audit": 1.5,
            "g2_contestability_override": 3.0,
            "g3_alert_fatigue_mitigation": 1.5,
            "g4_vendor_liability": 1.0,
            "g5_public_transparency": 1.0,
        }
    },

    "aarogya_setu": {
        "id": "aarogya_setu",
        "title": "Aarogya Setu Contact Tracing & Risk Zoning App",
        "domain": "Epidemic Surveillance, Digital Contact Tracing & Travel Pass",
        "implementer": "National Informatics Centre (NIC), Ministry of Electronics & IT, India",
        "deployment_scale": ">200 million smartphone downloads across India",
        "description": (
            "A national Bluetooth and GPS-driven mobile application launched during the first COVID-19 wave in India to track "
            "proximity to positive cases, calculate personal infection risk scores, and dynamically demarcate containment zones."
        ),
        "empirical_validation_citation": "Mukherjee et al. (2020), The Lancet Digital Health; Leslie (2020), Alan Turing Institute.",
        "failure_mode": (
            "Severe digital divide exclusion: In 2020, over 500 million Indians (predominantly rural, elderly, and female informal workers) "
            "did not own smartphones. Mandatory linkage to transit, office entry, and public services effectively created a digital "
            "caste barrier. Lack of initial open-source audit, centralized data pooling, and opaque risk score algorithms sparked "
            "major civil liberty and data security litigation."
        ),
        "ethical_tensions": [
            "Digital Divide & Disproportionate Burden: Excluded lower-income populations without smartphones from basic transit.",
            "Surveillance Overreach: Combined Bluetooth proximity with GPS geospatial coordinates, exceeding proportional necessity.",
            "Sunset Clause Vagueness: Indefinite retention of personal health data before eventual regulatory amendments."
        ],
        "default_scores": {
            "p1_clinical_need": 4.0,
            "p2_alternative_comparison": 3.0,
            "p3_stakeholder_engagement": 1.5,
            "p4_intended_context": 2.0,
            "p5_deontological_limits": 2.0,
            "d1_demographic_parity": 1.0, # Huge smartphone ownership skew (male/urban biased)
            "d2_label_fidelity": 3.0,
            "d3_temporal_shift": 3.0,
            "d4_missingness_bias": 1.5,
            "d5_data_privacy": 2.0,
            "a1_fairness_metric": 1.5,
            "a2_explainability": 2.5,
            "a3_calibration": 2.0,
            "a4_epistemic_uncertainty": 2.0,
            "a5_human_in_loop": 3.0,
            "g1_continuous_drift_audit": 2.5,
            "g2_contestability_override": 1.5,
            "g3_alert_fatigue_mitigation": 3.0,
            "g4_vendor_liability": 2.0,
            "g5_public_transparency": 2.5,
        }
    },

    "tb_chest_xray": {
        "id": "tb_chest_xray",
        "title": "AI-Assisted Chest X-Ray TB Screening (ICMR / qXR)",
        "domain": "Active Case Finding & Community Diagnostics for Tuberculosis",
        "implementer": "ICMR National Institute for Research in Tuberculosis & Qure.ai",
        "deployment_scale": "Nationwide active case finding vans in high-burden rural and tribal districts in India",
        "description": (
            "Deep learning computer vision algorithm deployed on mobile digital X-ray vans to detect pulmonary tuberculosis "
            "and cavitation in remote, resource-limited populations lacking on-site radiologists, triaging patients for rapid "
            "confirmatory GeneXpert molecular testing."
        ),
        "empirical_validation_citation": "ICMR Guidance on AI in TB (2022); Khan et al. (2020), Scientific Reports; Qin et al. (2021).",
        "failure_mode": (
            "Exemplary ethical design overall with high sensitivity (>93%). Minor limitations: algorithm had higher false-positive rates "
            "in elderly patients with healed prior TB scarring or silicosis/occupational lung disease, requiring careful confirmatory sputum protocol."
        ),
        "ethical_tensions": [
            "Equity & Beneficence Exemplar: Brought expert diagnostic screening directly to underserved tribal and rural regions.",
            "Human-in-the-Loop Safeguards: Explicitly used as a screening filter preceding molecular confirmation, preventing autonomous mistreatment.",
            "Subgroup Generalizability: Performance required calibration for low-dose portable X-ray hardware vs. high-resolution stationary hospital machines."
        ],
        "default_scores": {
            "p1_clinical_need": 5.0,
            "p2_alternative_comparison": 4.5,
            "p3_stakeholder_engagement": 4.5,
            "p4_intended_context": 4.5,
            "p5_deontological_limits": 4.5,
            "d1_demographic_parity": 4.0,
            "d2_label_fidelity": 4.5, # Microbiologically confirmed GeneXpert gold standard
            "d3_temporal_shift": 4.0,
            "d4_missingness_bias": 4.0,
            "d5_data_privacy": 4.5,
            "a1_fairness_metric": 4.0,
            "a2_explainability": 4.0, # Saliency heatmaps highlighting lung fields
            "a3_calibration": 4.5,
            "a4_epistemic_uncertainty": 3.5,
            "a5_human_in_loop": 5.0,
            "g1_continuous_drift_audit": 4.0,
            "g2_contestability_override": 4.5,
            "g3_alert_fatigue_mitigation": 4.5,
            "g4_vendor_liability": 4.0,
            "g5_public_transparency": 4.0,
        }
    },

    "ventilator_triage": {
        "id": "ventilator_triage",
        "title": "Crisis Standards of Care & Ventilator Triage Algorithms",
        "domain": "ICU Bed & Mechanical Ventilator Rationing under Crisis Surge",
        "implementer": "Multiple US State Health Depts & Hospital Triage Committees (SOFA-score scoring)",
        "deployment_scale": "State-level emergency health protocols adopted during COVID-19 surges (NY, MA, WA)",
        "description": (
            "Algorithmic decision rules and scoring systems (incorporating Sequential Organ Failure Assessment [SOFA] and "
            "underlying comorbidity penalties) designed to objectively ration scarce mechanical ventilators and ICU beds "
            "when acute demand exceeded physical capacity."
        ),
        "empirical_validation_citation": "White & Lo (2020), JAMA; Miller et al. (2021), AJRCCM; Schmidt (2020), Hastings Center Report.",
        "failure_mode": (
            "Algorithms systematically deprioritized Black, Hispanic, and disabled individuals. SOFA baseline renal metrics (creatinine) "
            "and comorbidity tiebreakers penalized groups suffering from long-standing structural disparities in chronic disease, "
            "effectively magnifying historical social discrimination into algorithmic death warrants."
        ),
        "ethical_tensions": [
            "Utilitarian Bias vs. Disability Rights: Calculating long-term life years directly discriminates against people with disabilities.",
            "Measurement Bias: Using biomarker cutoffs that reflect systemic healthcare access barriers rather than acute survivability.",
            "Lack of Participatory Justice: Crisis protocols were authored by academic bioethicists without representation from marginalized communities."
        ],
        "default_scores": {
            "p1_clinical_need": 4.5,
            "p2_alternative_comparison": 2.5,
            "p3_stakeholder_engagement": 1.5,
            "p4_intended_context": 2.0,
            "p5_deontological_limits": 1.5,
            "d1_demographic_parity": 1.0, # Structural racism embedded in comorbidity baselines
            "d2_label_fidelity": 2.5,
            "d3_temporal_shift": 2.0,
            "d4_missingness_bias": 2.0,
            "d5_data_privacy": 4.0,
            "a1_fairness_metric": 1.0, # Pure utilitarian survivor-years without anti-discrimination floor
            "a2_explainability": 3.0,
            "a3_calibration": 2.0,
            "a4_epistemic_uncertainty": 1.5,
            "a5_human_in_loop": 3.5,
            "g1_continuous_drift_audit": 1.5,
            "g2_contestability_override": 1.5,
            "g3_alert_fatigue_mitigation": 3.0,
            "g4_vendor_liability": 1.5,
            "g5_public_transparency": 3.0,
        }
    }
}
