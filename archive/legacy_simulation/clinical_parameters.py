"""
Empirical Clinical and Epidemiological Parameters for EpiEthic-AI.
Derived from peer-reviewed clinical epidemiological studies:
- Verity et al. (2020), Lancet Infectious Diseases: Age-stratified Infection Hospitalization & Critical Care Progression
- Ferguson et al. (2020), Imperial College London Report 9: Multi-cohort pandemic surge dynamics
- ICMR National Clinical Registry for COVID-19 (2021)
- WHO Therapeutics and COVID-19 Living Guideline
"""

CLINICAL_PARAMETERS = {
    # Stratified infection hospitalization rate (IHR) and Critical Care Case Fatality Rates (CFR)
    "cohort_clinical_profiles": {
        "C1_Youth": {
            "name": "Youth (0-19)",
            "susceptibility_multiplier": 0.70,   # Lower susceptibility
            "ihr": 0.008,                        # 0.8% of infections require hospitalization
            "icu_given_hosp": 0.08,              # 8% of hospitalized require ICU/oxygen
            "cfr_icu_optimal": 0.05,             # 5% mortality if ICU is available
            "cfr_icu_depleted": 0.40,            # 40% mortality if ICU is denied/unmet
            "avg_life_years_remaining": 65.0,    # Quality-adjusted life years remaining
        },
        "C2_Informal_Labor": {
            "name": "Working Adults / Informal Labor (20-59)",
            "susceptibility_multiplier": 1.15,   # High mobility & occupational density
            "ihr": 0.045,                        # 4.5% require hospitalization
            "icu_given_hosp": 0.22,              # 22% of hospitalized require ICU
            "cfr_icu_optimal": 0.16,             # 16% mortality with optimal ICU care
            "cfr_icu_depleted": 0.72,            # 72% mortality if ICU/oxygen is unavailable
            "avg_life_years_remaining": 38.0,    # Productive working life years
        },
        "C3_Elderly": {
            "name": "Elderly & Vulnerable (60+)",
            "susceptibility_multiplier": 1.35,   # Immunosenescence & comorbidities
            "ihr": 0.220,                        # 22.0% require hospitalization
            "icu_given_hosp": 0.42,              # 42% of hospitalized require ICU
            "cfr_icu_optimal": 0.38,             # 38% mortality even with full ICU care
            "cfr_icu_depleted": 0.94,            # 94% mortality if ICU is unavailable
            "avg_life_years_remaining": 14.0,    # Devalued under crude utilitarian models
        }
    },

    # Transmission and natural history parameters
    "disease_dynamics": {
        "r0_baseline": 2.6,
        "latent_period_days": 4.0,           # 1 / sigma (E -> I)
        "infectious_period_days": 5.5,       # 1 / gamma (I -> H or R)
        "hosp_stay_days": 8.0,               # Average duration in ward
        "icu_stay_days": 9.0,                # Average duration of critical care stay
    },

    # Intervention Efficacies (Vaccines & Antivirals)
    "intervention_efficacy": {
        "vaccine_transmission_reduction": 0.60, # Protection against infection transmission
        "vaccine_severe_disease_reduction": 0.88, # Protection against hospitalization & death
        "antiviral_death_reduction": 0.65,        # Mortality risk reduction if treated early
    }
}
