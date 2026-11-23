/**
 * EpiEthic-AI — Operational Lifecycle Ethics Scorecard Tool (JavaScript)
 * Harmonizing WHO (2021), ICMR (2023), and FUTURE-AI (Lekadir et al. 2021)
 */

const CASE_STUDIES = {
    "brfss_screening": {
        id: "brfss_screening",
        title: "CDC BRFSS AI Chronic Disease Screening Model (Our System)",
        domain: "Public Health Population Screening & Preventive Triage",
        implementer: "Public Health Authority / Computational Epidemiology Lab",
        scale: "Trained on 253,680 CDC BRFSS Patient Records",
        citation: "Empirical Group DRO & Differential Privacy Evaluation (2026)",
        description: "An ethically-constrained machine learning triage system identifying individuals with undiagnosed or high-risk chronic metabolic conditions to direct targeted community preventive screening.",
        failure_mode: "Mitigated by design: Utilitarian ERM models penalized vulnerable low-income patients (disparity gap 0.1719). Our Rawlsian Minimax formulation actively constrains worst-off group loss while Differential Privacy provides formal data guarantees.",
        scores: {
            p1: 5.0, p2: 4.5, p3: 4.0, p4: 4.5, p5: 4.5,
            d1: 4.5, d2: 4.5, d3: 4.0, d4: 4.0, d5: 4.5,
            a1: 4.5, a2: 4.0, a3: 4.5, a4: 3.5, a5: 4.5,
            g1: 4.0, g2: 4.0, g3: 4.0, g4: 3.5, g5: 4.0
        }
    },
    "epic_sepsis": {
        id: "epic_sepsis",
        title: "Epic Sepsis Model (ESM)",
        domain: "In-Hospital Acute Triage",
        implementer: "Epic Systems",
        scale: ">27,000 patient beds across dozens of US & international health systems",
        citation: "Wong et al. (2021), JAMA Internal Medicine",
        description: "A proprietary machine learning model built into the world's most widely used electronic health record (EHR) system. Predicts sepsis to prompt antibiotic and ICU escalation.",
        failure_mode: "Independent external validation showed discriminative performance collapse (AUROC dropped from claimed 0.76-0.83 to 0.63). Missed 67% of sepsis cases while generating an 88% false alarm rate, inducing severe clinical alert fatigue.",
        scores: {
            p1: 4.5, p2: 2.0, p3: 1.5, p4: 2.5, p5: 2.0,
            d1: 2.0, d2: 1.5, d3: 2.0, d4: 2.0, d5: 4.0,
            a1: 1.5, a2: 2.0, a3: 1.5, a4: 1.0, a5: 2.5,
            g1: 1.5, g2: 3.0, g3: 1.5, g4: 1.0, g5: 1.0
        }
    },
    "aarogya_setu": {
        id: "aarogya_setu",
        title: "Aarogya Setu Contact Tracing & Risk Zoning App",
        domain: "Epidemic Surveillance & Travel Pass",
        implementer: "National Informatics Centre (NIC), Ministry of Electronics & IT, India",
        scale: ">200 million smartphone downloads across India",
        citation: "Mukherjee et al. (2020), The Lancet Digital Health; Leslie (2020)",
        description: "National Bluetooth and GPS-driven mobile application launched during COVID-19 to calculate personal infection risk scores and demarcate containment zones.",
        failure_mode: "Severe digital divide exclusion: ~500 million Indians without smartphones were blocked from transit and work. Opaque risk scores and centralized data pooling raised major constitutional privacy and proportionality litigation.",
        scores: {
            p1: 4.0, p2: 3.0, p3: 1.5, p4: 2.0, p5: 2.0,
            d1: 1.0, d2: 3.0, d3: 3.0, d4: 1.5, d5: 2.0,
            a1: 1.5, a2: 2.5, a3: 2.0, a4: 2.0, a5: 3.0,
            g1: 2.5, g2: 1.5, g3: 3.0, g4: 2.0, g5: 2.5
        }
    },
    "tb_chest_xray": {
        id: "tb_chest_xray",
        title: "AI-Assisted Chest X-Ray TB Screening (ICMR / qXR)",
        domain: "Active Case Finding & Community Diagnostics",
        implementer: "ICMR National Institute for Research in TB & Qure.ai",
        scale: "Nationwide active case finding mobile vans in high-burden rural and tribal districts",
        citation: "ICMR Guidance on AI in TB (2022); Khan et al. (2020)",
        description: "Deep learning computer vision deployed on mobile digital X-ray vans to detect pulmonary TB in underserved populations, triaging patients for confirmatory GeneXpert molecular testing.",
        failure_mode: "Exemplary high sensitivity (>93%). Minor limitations: elevated false-positive rates in elderly patients with healed prior TB scarring or silicosis, requiring strict confirmatory sputum protocols.",
        scores: {
            p1: 5.0, p2: 4.5, p3: 4.5, p4: 4.5, p5: 4.5,
            d1: 4.0, d2: 4.5, d3: 4.0, d4: 4.0, d5: 4.5,
            a1: 4.0, a2: 4.0, a3: 4.5, a4: 3.5, a5: 5.0,
            g1: 4.0, g2: 4.5, g3: 4.5, g4: 4.0, g5: 4.0
        }
    },
    "ventilator_triage": {
        id: "ventilator_triage",
        title: "Crisis Standards of Care & Ventilator Triage Algorithms",
        domain: "Emergency ICU & Mechanical Ventilator Rationing",
        implementer: "Hospital Triage Committees & State Health Depts (SOFA Protocols)",
        scale: "State-level emergency crisis health protocols adopted during COVID-19 surges",
        citation: "White & Lo (2020), JAMA; Schmidt (2020), Hastings Center Report",
        description: "Scoring algorithms utilizing Sequential Organ Failure Assessment (SOFA) and comorbidity tie-breakers to allocate ventilators when demand overwhelmed hospital capacity.",
        failure_mode: "Systematically penalized Black, Hispanic, and disabled individuals. Creatinine cutoffs and chronic comorbidity penalties amplified historical health disparities into automated death warrants.",
        scores: {
            p1: 4.5, p2: 2.5, p3: 1.5, p4: 2.0, p5: 1.5,
            d1: 1.0, d2: 2.5, d3: 2.0, d4: 2.0, d5: 4.0,
            a1: 1.0, a2: 3.0, a3: 2.0, a4: 1.5, a5: 3.5,
            g1: 1.5, g2: 1.5, g3: 3.0, g4: 1.5, g5: 3.0
        }
    }
};

const LIFECYCLE_STAGES_CONFIG = [
    {
        id: "stage_1",
        title: "Stage 1: Problem Formulation & Epistemic Justification",
        sources: "WHO (2021) Principle 1 & 4; ICMR (2023) Section 2; Floridi et al. (2018)",
        metrics: [
            { id: "p1", name: "Public Health Necessity & Proportionality", weight: 1.0 },
            { id: "p2", name: "Benchmarking vs. Simpler Clinical Heuristics", weight: 1.0 },
            { id: "p3", name: "Participatory Design with Marginalized Groups", weight: 1.2 },
            { id: "p4", name: "Contextual Feasibility in Target Health Facilities", weight: 0.8 },
            { id: "p5", name: "Non-Negotiable Human Rights & Override Red-Lines", weight: 1.2 }
        ]
    },
    {
        id: "stage_2",
        title: "Stage 2: Data Provenance, Representativeness & Privacy",
        sources: "ICMR (2023) Section 3; FUTURE-AI (Universality); WHO Principle 2",
        metrics: [
            { id: "d1", name: "Demographic & Socioeconomic Dataset Diversity", weight: 1.3 },
            { id: "d2", name: "Gold-Standard Ground Truth vs. Proxy Confounding", weight: 1.2 },
            { id: "d3", name: "Temporal Strain Shift & Epidemiologic Robustness", weight: 1.0 },
            { id: "d4", name: "Missing Clinical Data & Diagnostic Inequity Audit", weight: 1.0 },
            { id: "d5", name: "Differential Privacy & Informed Institutional Consent", weight: 1.0 }
        ]
    },
    {
        id: "stage_3",
        title: "Stage 3: Algorithmic Optimization & Distributive Fairness",
        sources: "WHO Principle 3 (Equity); Kleinberg et al. (2016); FUTURE-AI",
        metrics: [
            { id: "a1", name: "Formal Mathematical Group Fairness Constraints", weight: 1.3 },
            { id: "a2", name: "Clinically Interpretable Explanations (SHAP/Saliency)", weight: 1.0 },
            { id: "a3", name: "Multi-Subgroup Risk Calibration & Error Parity", weight: 1.1 },
            { id: "a4", name: "Epistemic Uncertainty & 'I Don't Know' Capability", weight: 1.0 },
            { id: "a5", name: "Human Agency & Frictionless Physician Override", weight: 1.2 }
        ]
    },
    {
        id: "stage_4",
        title: "Stage 4: Post-Market Governance, Contestability & Drift",
        sources: "WHO Principle 5 & 6 (Sustainability & Accountability); ICMR Section 5",
        metrics: [
            { id: "g1", name: "Continuous Performance & Fairness Drift Monitoring", weight: 1.2 },
            { id: "g2", name: "Patient Contestability & Clinical Appeals Route", weight: 1.2 },
            { id: "g3", name: "Clinical Alert Fatigue & Ergonomic Burden Audit", weight: 0.9 },
            { id: "g4", name: "Legal Liability Delineation (Vendor vs. Hospital)", weight: 1.1 },
            { id: "g5", name: "Public Trial Registration & Open Code Transparency", weight: 1.0 }
        ]
    }
];

function evaluateLifecycleScores(userScores) {
    let stageResults = [];
    let totalWeighted = 0;
    let totalMax = 0;

    for (let stage of LIFECYCLE_STAGES_CONFIG) {
        let stagePts = 0;
        let stageMax = 0;
        for (let m of stage.metrics) {
            let s = userScores[m.id] !== undefined ? userScores[m.id] : 3.0;
            stagePts += s * m.weight;
            stageMax += 5.0 * m.weight;
        }
        let pct = (stagePts / stageMax) * 100.0;
        stageResults.push({
            id: stage.id,
            title: stage.title.split(":")[1].trim(),
            percentage: Math.round(pct * 10) / 10,
            score: Math.round(stagePts * 10) / 10,
            max: Math.round(stageMax * 10) / 10
        });
        totalWeighted += stagePts;
        totalMax += stageMax;
    }

    let overallPct = Math.round((totalWeighted / totalMax) * 1000) / 10;
    let tier = "";
    let directive = "";

    if (overallPct >= 80.0) {
        tier = "Ethically Robust (Low Risk)";
        directive = "System meets high standards across WHO and ICMR guidelines. Safe for phased clinical deployment.";
    } else if (overallPct >= 60.0) {
        tier = "Conditional Approval (Moderate Ethical Risk)";
        directive = "Notable gaps in subgroup fairness, contestability, or data provenance. Requires mitigation before deployment.";
    } else {
        tier = "High Ethical Risk (Deployment Halted)";
        directive = "Critical violations of non-discrimination, transparency, or human agency. Significant harm potential.";
    }

    return {
        overallPercentage: overallPct,
        tier: tier,
        directive: directive,
        stages: stageResults
    };
}
