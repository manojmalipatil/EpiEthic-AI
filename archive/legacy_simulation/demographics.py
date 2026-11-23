"""
Real Demographic Profiles and Capacity Parameters for EpiEthic-AI.
Data sources:
- Census of India & National Family Health Survey (NFHS-5, 2019-2021)
- National Health Profile (NHP, MoHFW, Govt of India)
- CDC / US Census Bureau (for international comparison scenario)
"""

DEMOGRAPHIC_PROFILES = {
    "India_Urban_Metro": {
        "name": "Indian Urban Metro (e.g., Mumbai / Bengaluru / Delhi)",
        "source": "Census of India, NFHS-5 (2019-2021), MoHFW Health Profile",
        "description": "High density, mixed socioeconomic strata with large informal labor force and concentrated tertiary healthcare.",
        "total_population": 1_000_000,
        "cohorts": {
            "C1_Youth": {
                "label": "Youth & Children (0-19 yrs)",
                "fraction": 0.32,
                "density_factor": 1.1,
                "comorbidity_prevalence": 0.04,
                "socioeconomic_vulnerability": "Low",
                "baseline_access_factor": 1.0,
            },
            "C2_Informal_Labor": {
                "label": "Working Adults / Informal Labor (20-59 yrs)",
                "fraction": 0.58,
                "density_factor": 1.4,  # Crowded transit, informal settlements, high daily exposure
                "comorbidity_prevalence": 0.18, # Diabetes, hypertension (NFHS-5 urban estimates)
                "socioeconomic_vulnerability": "High",
                "baseline_access_factor": 0.7, # Lower insurance, out-of-pocket barrier
            },
            "C3_Elderly": {
                "label": "Elderly & Vulnerable (60+ yrs)",
                "fraction": 0.10,
                "density_factor": 0.8,
                "comorbidity_prevalence": 0.52, # High cardiovascular / respiratory / metabolic
                "socioeconomic_vulnerability": "Critical",
                "baseline_access_factor": 0.85,
            }
        },
        "resources": {
            "icu_beds_per_100k": 25.0,     # Higher urban concentration
            "regular_beds_per_100k": 140.0,
            "daily_vaccine_capacity": 5000, # 0.5% pop/day
            "daily_antiviral_doses": 1200
        }
    },
    "India_Rural_District": {
        "name": "Indian Rural District (e.g., Gorakhpur / Kalahandi)",
        "source": "National Health Profile, MoHFW Rural Health Statistics (2021-22)",
        "description": "Lower critical care density, high distance barrier, younger demographic with high under-diagnosed comorbidities.",
        "total_population": 1_000_000,
        "cohorts": {
            "C1_Youth": {
                "label": "Youth & Children (0-19 yrs)",
                "fraction": 0.38,
                "density_factor": 0.9,
                "comorbidity_prevalence": 0.06,
                "socioeconomic_vulnerability": "Medium",
                "baseline_access_factor": 0.6,
            },
            "C2_Informal_Labor": {
                "label": "Agrarian & Informal Workers (20-59 yrs)",
                "fraction": 0.54,
                "density_factor": 1.0,
                "comorbidity_prevalence": 0.14,
                "socioeconomic_vulnerability": "High",
                "baseline_access_factor": 0.5,
            },
            "C3_Elderly": {
                "label": "Elderly (60+ yrs)",
                "fraction": 0.08,
                "density_factor": 0.7,
                "comorbidity_prevalence": 0.44,
                "socioeconomic_vulnerability": "High",
                "baseline_access_factor": 0.45,
            }
        },
        "resources": {
            "icu_beds_per_100k": 4.5,      # Critical rural shortage
            "regular_beds_per_100k": 45.0,
            "daily_vaccine_capacity": 2500,
            "daily_antiviral_doses": 400
        }
    },
    "Global_Aging_Demographic": {
        "name": "High-Income Aging Metropolitan (e.g., Milan / Tokyo / NYC)",
        "source": "WHO World Health Statistics & CDC National Vital Statistics",
        "description": "Inverted population pyramid with heavy elderly cohort (23%), robust tertiary ICU baseline.",
        "total_population": 1_000_000,
        "cohorts": {
            "C1_Youth": {
                "label": "Youth (0-19 yrs)",
                "fraction": 0.18,
                "density_factor": 0.8,
                "comorbidity_prevalence": 0.03,
                "socioeconomic_vulnerability": "Low",
                "baseline_access_factor": 1.0,
            },
            "C2_Informal_Labor": {
                "label": "Working Adults (20-59 yrs)",
                "fraction": 0.59,
                "density_factor": 1.1,
                "comorbidity_prevalence": 0.16,
                "socioeconomic_vulnerability": "Medium",
                "baseline_access_factor": 0.95,
            },
            "C3_Elderly": {
                "label": "Elderly (60+ yrs)",
                "fraction": 0.23,
                "density_factor": 0.9,
                "comorbidity_prevalence": 0.61,
                "socioeconomic_vulnerability": "High",
                "baseline_access_factor": 0.90,
            }
        },
        "resources": {
            "icu_beds_per_100k": 32.0,
            "regular_beds_per_100k": 280.0,
            "daily_vaccine_capacity": 7500,
            "daily_antiviral_doses": 2500
        }
    }
}
