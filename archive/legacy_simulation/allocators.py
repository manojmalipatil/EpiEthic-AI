"""
Ethical Resource Allocators for EpiEthic-AI.
Formal mathematical implementations of four distributive justice frameworks:
1. Utilitarian (Bentham / Mill: Maximize total lives or QALYs saved)
2. Rawlsian Prioritarian (Rawls / Daniels: Maximin - prioritize the worst-off cohort)
3. Egalitarian (Equal per-capita / Demographic parity lottery)
4. Privacy-Preserving Surveillance (Differentially private noisy surveillance allocation)
"""

import numpy as np
from typing import Dict, Any

class EthicalAllocator:
    """Base class for public health resource allocators."""
    def __init__(self, name: str, philosophy: str, core_principle: str):
        self.name = name
        self.philosophy = philosophy
        self.core_principle = core_principle

    def allocate(
        self,
        resource_type: str,
        total_available: float,
        cohort_states: Dict[str, Dict[str, float]],
        clinical_params: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, float]:
        raise NotImplementedError


class UtilitarianAllocator(EthicalAllocator):
    """
    Utilitarian / Consequentialist Paradigm (Bentham, Mill).
    Objective: Maximize total aggregate net lives saved (or QALYs).
    Allocates scarce ICU beds and vaccines where the marginal reduction in mortality
    per unit of intervention is maximized.
    """
    def __init__(self, optimize_for: str = "lives_saved"):
        super().__init__(
            name="Utilitarian (Max Net Benefit)",
            philosophy="Consequentialism / Utilitarianism (Bentham, Mill)",
            core_principle="Maximize aggregate welfare; allocate where marginal lives saved per unit resource is highest."
        )
        self.optimize_for = optimize_for  # "lives_saved" or "qalys"

    def allocate(
        self,
        resource_type: str,
        total_available: float,
        cohort_states: Dict[str, Dict[str, float]],
        clinical_params: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, float]:
        if total_available <= 0:
            return {c: 0.0 for c in cohort_states}

        marginal_gains = {}
        demands = {}

        for c_id, state in cohort_states.items():
            clin = clinical_params["cohort_clinical_profiles"][c_id]
            demand = 0.0
            unit_gain = 0.0

            if resource_type == "icu_beds":
                demand = state.get("active_critical_demand", 0.0)
                # Gain = delta death rate averted if given ICU vs depleted
                delta_cfr = max(0.01, clin["cfr_icu_depleted"] - clin["cfr_icu_optimal"])
                if self.optimize_for == "qalys":
                    unit_gain = delta_cfr * clin["avg_life_years_remaining"]
                else:
                    unit_gain = delta_cfr

            elif resource_type == "vaccines":
                demand = state.get("S", 0.0)
                # Severe risk per infection
                severe_risk = clin["ihr"] * clin["icu_given_hosp"] * clin["cfr_icu_depleted"]
                if self.optimize_for == "qalys":
                    unit_gain = severe_risk * clin["avg_life_years_remaining"]
                else:
                    unit_gain = severe_risk

            marginal_gains[c_id] = max(1e-4, unit_gain)
            demands[c_id] = max(0.0, demand)

        # Allocate greedily to highest marginal return
        sorted_cohorts = sorted(marginal_gains.keys(), key=lambda c: marginal_gains[c], reverse=True)
        allocations = {c: 0.0 for c in cohort_states}
        remaining_budget = total_available

        for c in sorted_cohorts:
            alloc = min(remaining_budget, demands[c])
            allocations[c] = alloc
            remaining_budget -= alloc
            if remaining_budget <= 0:
                break

        # Distribute any residual budget according to marginal gain proportion
        if remaining_budget > 0:
            tot_g = sum(marginal_gains.values())
            for c in cohort_states:
                allocations[c] += remaining_budget * (marginal_gains[c] / tot_g)

        return allocations


class RawlsianMaximinAllocator(EthicalAllocator):
    """
    Rawlsian / Prioritarian Paradigm (Rawls, Daniels, Persad).
    Objective: Maximin - prioritize the worst-off cohort to minimize inter-group health inequality.
    The worst-off cohort is determined dynamically by active cumulative mortality rate and intrinsic vulnerability.
    """
    def __init__(self):
        super().__init__(
            name="Rawlsian Prioritarian (Equity-First)",
            philosophy="Deontological Prioritarianism / Distributive Justice (Rawls, Daniels)",
            core_principle="Inequalities are justifiable only if they maximize the position of the least advantaged."
        )

    def allocate(
        self,
        resource_type: str,
        total_available: float,
        cohort_states: Dict[str, Dict[str, float]],
        clinical_params: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, float]:
        if total_available <= 0:
            return {c: 0.0 for c in cohort_states}

        vulnerability_scores = {}
        demands = {}

        for c_id, state in cohort_states.items():
            clin = clinical_params["cohort_clinical_profiles"][c_id]
            pop = state.get("N", 1.0)
            deaths = state.get("D", 0.0)
            current_mortality_rate = deaths / max(1.0, pop)

            # Combined baseline vulnerability and current mortality burden
            vulnerability_scores[c_id] = (clin["cfr_icu_depleted"] * 2.0) + (current_mortality_rate * 100.0)

            if resource_type == "icu_beds":
                demands[c_id] = state.get("active_critical_demand", 0.0)
            elif resource_type == "vaccines":
                demands[c_id] = state.get("S", 0.0)

        # Sort worst-off first
        sorted_cohorts = sorted(vulnerability_scores.keys(), key=lambda c: vulnerability_scores[c], reverse=True)
        allocations = {c: 0.0 for c in cohort_states}
        remaining_budget = total_available

        # Prioritize the most disadvantaged group's demand completely before lower-risk cohorts
        for c in sorted_cohorts:
            alloc = min(remaining_budget, demands[c])
            allocations[c] = alloc
            remaining_budget -= alloc
            if remaining_budget <= 0:
                break

        if remaining_budget > 0:
            tot_v = sum(vulnerability_scores[c] for c in sorted_cohorts)
            for c in sorted_cohorts:
                allocations[c] += remaining_budget * (vulnerability_scores[c] / tot_v)

        return allocations


class EgalitarianAllocator(EthicalAllocator):
    """
    Egalitarian Paradigm (Demographic Parity / Fair Lottery).
    Objective: Strict equality of per-capita access.
    Every demographic group receives an allocation exactly equal to their proportion of the total population,
    irrespective of risk differentials or clinical prognosis.
    """
    def __init__(self):
        super().__init__(
            name="Egalitarian (Demographic Parity)",
            philosophy="Strict Egalitarianism / Procedural Fairness",
            core_principle="Treat every person with identical formal equality; allocate strictly per-capita."
        )

    def allocate(
        self,
        resource_type: str,
        total_available: float,
        cohort_states: Dict[str, Dict[str, float]],
        clinical_params: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, float]:
        if total_available <= 0:
            return {c: 0.0 for c in cohort_states}

        total_pop = sum(state.get("N", 1.0) for state in cohort_states.values())
        allocations = {}
        for c_id, state in cohort_states.items():
            pop_fraction = state.get("N", 1.0) / max(1.0, total_pop)
            allocations[c_id] = total_available * pop_fraction

        return allocations


class PrivacyPreservingAllocator(EthicalAllocator):
    """
    Privacy-Constrained Surveillance Paradigm (Differential Privacy Noise).
    Objective: Allocation driven by disease surveillance where reported counts are masked by
    Laplace noise under (epsilon)-Differential Privacy.
    Demonstrates how data privacy guarantees can perturb resource targeting.
    """
    def __init__(self, epsilon: float = 1.0):
        super().__init__(
            name=f"Privacy-Preserving (DP $\\epsilon={epsilon}$)",
            philosophy="Informational Self-Determination & Epistemic Uncertainty (Dwork)",
            core_principle="Surveillance data must protect patient anonymity via provable differential privacy noise."
        )
        self.epsilon = max(0.05, float(epsilon))

    def allocate(
        self,
        resource_type: str,
        total_available: float,
        cohort_states: Dict[str, Dict[str, float]],
        clinical_params: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, float]:
        if total_available <= 0:
            return {c: 0.0 for c in cohort_states}

        scale = 1.0 / self.epsilon
        noisy_signals = {}
        for c_id, state in cohort_states.items():
            if resource_type == "icu_beds":
                raw = state.get("active_critical_demand", 0.0)
            elif resource_type == "vaccines":
                raw = state.get("I", 0.0) * 1.2 + state.get("S", 0.0) * 0.1
            else:
                raw = state.get("I", 0.0)

            # Laplace noise perturbation
            noise = np.random.laplace(0.0, scale * (raw * 0.12 + 8.0))
            noisy_signals[c_id] = max(1.0, raw + noise)

        tot_noisy = sum(noisy_signals.values())
        allocations = {}
        for c_id in cohort_states:
            fraction = noisy_signals[c_id] / max(1.0, tot_noisy)
            allocations[c_id] = total_available * fraction

        return allocations
