"""
Dynamic Outbreak and Allocation Simulation Engine for EpiEthic-AI.
Extended multi-cohort SEIR-HCD model with dynamic resource allocation:
S: Susceptible
E: Exposed
I: Infectious
R: Recovered
H: Hospitalized (Ward)
C: Critical (Needing ICU / Ventilator)
D: Deceased
"""

import numpy as np
from typing import Dict, Any
from src.allocators import EthicalAllocator

class OutbreakSimulation:
    def __init__(
        self,
        demographic_profile: Dict[str, Any],
        clinical_params: Dict[str, Any],
        allocator: EthicalAllocator,
        duration_days: int = 120,
        initial_infected_fraction: float = 0.001
    ):
        self.demo = demographic_profile
        self.clin = clinical_params
        self.allocator = allocator
        self.duration_days = duration_days
        self.initial_infected_fraction = initial_infected_fraction
        self.total_pop = demographic_profile["total_population"]
        self.cohorts = demographic_profile["cohorts"]

    def run(self) -> Dict[str, Any]:
        """
        Executes daily step-wise epidemic simulation with dynamic ethical allocation.
        """
        cohort_keys = list(self.cohorts.keys())
        days = self.duration_days
        
        # Epidemiological parameters
        r0 = self.clin["disease_dynamics"]["r0_baseline"]
        sigma = 1.0 / self.clin["disease_dynamics"]["latent_period_days"]
        gamma = 1.0 / self.clin["disease_dynamics"]["infectious_period_days"]
        beta_base = r0 * gamma
        
        # Critical resource caps
        icu_capacity = (self.demo["resources"]["icu_beds_per_100k"] / 100_000.0) * self.total_pop
        daily_vaccine_budget = self.demo["resources"]["daily_vaccine_capacity"]

        # History recorder
        history = {
            "days": list(range(days)),
            "susceptible": {c: np.zeros(days) for c in cohort_keys},
            "exposed": {c: np.zeros(days) for c in cohort_keys},
            "infections": {c: np.zeros(days) for c in cohort_keys},
            "recovered": {c: np.zeros(days) for c in cohort_keys},
            "hospitalized": {c: np.zeros(days) for c in cohort_keys},
            "critical_icu": {c: np.zeros(days) for c in cohort_keys},
            "deaths": {c: np.zeros(days) for c in cohort_keys},
            "allocations_icu": {c: np.zeros(days) for c in cohort_keys},
            "allocations_vax": {c: np.zeros(days) for c in cohort_keys},
            "unmet_icu_days": np.zeros(days),
            "icu_capacity_line": icu_capacity,
        }

        # Initialize cohort states
        state = {}
        for c in cohort_keys:
            cohort_n = self.cohorts[c]["fraction"] * self.total_pop
            init_i = max(5.0, cohort_n * self.initial_infected_fraction * self.cohorts[c]["density_factor"])
            state[c] = {
                "N": cohort_n,
                "S": cohort_n - init_i,
                "E": 0.0,
                "I": init_i,
                "R": 0.0,
                "H": 0.0,
                "C": 0.0,
                "D": 0.0,
                "active_critical_demand": 0.0,
                "vaccinated": 0.0
            }

        # Daily simulation loop
        for t in range(days):
            # 1. Allocate scarce resources based on current ethical philosophy
            allocated_icu = self.allocator.allocate(
                resource_type="icu_beds",
                total_available=icu_capacity,
                cohort_states=state,
                clinical_params=self.clin
            )

            allocated_vax = self.allocator.allocate(
                resource_type="vaccines",
                total_available=daily_vaccine_budget,
                cohort_states=state,
                clinical_params=self.clin
            )

            day_unmet_icu = 0.0
            total_active_I = sum(state[c]["I"] for c in cohort_keys)
            force_of_infection = (beta_base * total_active_I) / self.total_pop

            for c in cohort_keys:
                c_data = self.cohorts[c]
                c_clin = self.clin["cohort_clinical_profiles"][c]

                # Log state today
                history["susceptible"][c][t] = state[c]["S"]
                history["exposed"][c][t] = state[c]["E"]
                history["infections"][c][t] = state[c]["I"]
                history["recovered"][c][t] = state[c]["R"]
                history["hospitalized"][c][t] = state[c]["H"]
                history["critical_icu"][c][t] = state[c]["C"]
                history["deaths"][c][t] = state[c]["D"]
                history["allocations_icu"][c][t] = allocated_icu.get(c, 0.0)
                history["allocations_vax"][c][t] = allocated_vax.get(c, 0.0)

                # Step A: Vaccinations
                vax_units = allocated_vax.get(c, 0.0)
                actual_vax = min(state[c]["S"], vax_units)
                state[c]["S"] -= actual_vax
                state[c]["R"] += actual_vax * self.clin["intervention_efficacy"]["vaccine_severe_disease_reduction"]
                state[c]["vaccinated"] += actual_vax

                # Step B: Transmission (S -> E)
                cohort_trans_risk = force_of_infection * c_data["density_factor"] * c_clin["susceptibility_multiplier"]
                new_exposed = min(state[c]["S"], cohort_trans_risk * state[c]["S"])

                # Step C: Progression (E -> I)
                new_infectious = sigma * state[c]["E"]

                # Step D: Resolution of Infectious (I -> Hosp or Recovery)
                hosp_fraction = c_clin["ihr"]
                new_hosp = gamma * state[c]["I"] * hosp_fraction
                new_mild_recovered = gamma * state[c]["I"] * (1.0 - hosp_fraction)

                # Step E: Progression to Critical ICU need
                crit_fraction = c_clin["icu_given_hosp"]
                new_critical_admissions = new_hosp * crit_fraction
                state[c]["active_critical_demand"] += new_critical_admissions

                # Step F: ICU Allocation and Clinical Outcomes
                assigned_beds = allocated_icu.get(c, 0.0)
                admitted_icu = min(state[c]["active_critical_demand"], assigned_beds)
                unmet_critical = max(0.0, state[c]["active_critical_demand"] - assigned_beds)
                day_unmet_icu += unmet_critical

                # Mortality from critical patients:
                # Critical duration ~9 days
                crit_exit_rate = 1.0 / self.clin["disease_dynamics"]["icu_stay_days"]
                exiting_admitted = admitted_icu * crit_exit_rate
                exiting_unmet = unmet_critical * crit_exit_rate

                deaths_from_admitted = exiting_admitted * c_clin["cfr_icu_optimal"]
                recovered_from_admitted = exiting_admitted * (1.0 - c_clin["cfr_icu_optimal"])

                deaths_from_unmet = exiting_unmet * c_clin["cfr_icu_depleted"]
                recovered_from_unmet = exiting_unmet * (1.0 - c_clin["cfr_icu_depleted"])

                daily_new_deaths = deaths_from_admitted + deaths_from_unmet
                daily_new_crit_recovered = recovered_from_admitted + recovered_from_unmet

                # Step G: Compartment Balance Updates
                state[c]["S"] = max(0.0, state[c]["S"] - new_exposed)
                state[c]["E"] = max(0.0, state[c]["E"] + new_exposed - new_infectious)
                state[c]["I"] = max(0.0, state[c]["I"] + new_infectious - (new_mild_recovered + new_hosp))
                state[c]["H"] = max(0.0, state[c]["H"] + new_hosp - new_critical_admissions)
                state[c]["C"] = admitted_icu
                state[c]["active_critical_demand"] = max(0.0, state[c]["active_critical_demand"] - (exiting_admitted + exiting_unmet))
                state[c]["R"] = state[c]["R"] + new_mild_recovered + daily_new_crit_recovered
                state[c]["D"] = state[c]["D"] + daily_new_deaths

            history["unmet_icu_days"][t] = day_unmet_icu

        return history
