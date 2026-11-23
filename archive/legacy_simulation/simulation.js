/**
 * EpiEthic-AI — Core Epidemiological & Allocation Simulation Engine (JavaScript)
 * Real Empirical Data: NFHS-5, Indian Census, Lancet Infectious Diseases (Verity et al. 2020)
 */

const DEMOGRAPHIC_PROFILES = {
    "India_Urban_Metro": {
        name: "Indian Urban Metro (Mumbai / Bengaluru / Delhi)",
        source: "Census of India, NFHS-5 (2019-2021), MoHFW Health Profile",
        description: "High density, 58% informal working adults, 10% elderly (52% comorbidities).",
        total_population: 1000000,
        cohorts: {
            "C1_Youth": {
                label: "Youth (0-19)",
                fraction: 0.32,
                density_factor: 1.1,
                comorbidity_prevalence: 0.04
            },
            "C2_Informal_Labor": {
                label: "Working Adults (20-59)",
                fraction: 0.58,
                density_factor: 1.4,
                comorbidity_prevalence: 0.18
            },
            "C3_Elderly": {
                label: "Elderly & Vulnerable (60+)",
                fraction: 0.10,
                density_factor: 0.8,
                comorbidity_prevalence: 0.52
            }
        },
        resources: {
            icu_beds_per_100k: 25.0,
            daily_vaccine_capacity: 5000
        }
    },
    "India_Rural_District": {
        name: "Indian Rural District (Gorakhpur / Kalahandi)",
        source: "MoHFW Rural Health Statistics (2021-22)",
        description: "Severe critical care shortage (4.5 beds/100k), 38% youth, high distance barriers.",
        total_population: 1000000,
        cohorts: {
            "C1_Youth": {
                label: "Youth (0-19)",
                fraction: 0.38,
                density_factor: 0.9,
                comorbidity_prevalence: 0.06
            },
            "C2_Informal_Labor": {
                label: "Agrarian Workers (20-59)",
                fraction: 0.54,
                density_factor: 1.0,
                comorbidity_prevalence: 0.14
            },
            "C3_Elderly": {
                label: "Elderly (60+)",
                fraction: 0.08,
                density_factor: 0.7,
                comorbidity_prevalence: 0.44
            }
        },
        resources: {
            icu_beds_per_100k: 4.5,
            daily_vaccine_capacity: 2500
        }
    },
    "Global_Aging": {
        name: "High-Income Aging Metro (Milan / Tokyo / NYC)",
        source: "WHO World Health Statistics & CDC Vital Stats",
        description: "Inverted demographic pyramid (23% elderly), abundant tertiary ICU baseline.",
        total_population: 1000000,
        cohorts: {
            "C1_Youth": {
                label: "Youth (0-19)",
                fraction: 0.18,
                density_factor: 0.8,
                comorbidity_prevalence: 0.03
            },
            "C2_Informal_Labor": {
                label: "Working Adults (20-59)",
                fraction: 0.59,
                density_factor: 1.1,
                comorbidity_prevalence: 0.16
            },
            "C3_Elderly": {
                label: "Elderly (60+)",
                fraction: 0.23,
                density_factor: 0.9,
                comorbidity_prevalence: 0.61
            }
        },
        resources: {
            icu_beds_per_100k: 32.0,
            daily_vaccine_capacity: 7500
        }
    }
};

const CLINICAL_PARAMETERS = {
    cohort_clinical_profiles: {
        "C1_Youth": {
            name: "Youth (0-19)",
            susceptibility_multiplier: 0.70,
            ihr: 0.008,
            icu_given_hosp: 0.08,
            cfr_icu_optimal: 0.05,
            cfr_icu_depleted: 0.40,
            avg_life_years_remaining: 65.0
        },
        "C2_Informal_Labor": {
            name: "Working Adults (20-59)",
            susceptibility_multiplier: 1.15,
            ihr: 0.045,
            icu_given_hosp: 0.22,
            cfr_icu_optimal: 0.16,
            cfr_icu_depleted: 0.72,
            avg_life_years_remaining: 38.0
        },
        "C3_Elderly": {
            name: "Elderly & Vulnerable (60+)",
            susceptibility_multiplier: 1.35,
            ihr: 0.220,
            icu_given_hosp: 0.42,
            cfr_icu_optimal: 0.38,
            cfr_icu_depleted: 0.94,
            avg_life_years_remaining: 14.0
        }
    },
    disease_dynamics: {
        r0_baseline: 2.6,
        latent_period_days: 4.0,
        infectious_period_days: 5.5,
        icu_stay_days: 9.0
    },
    intervention_efficacy: {
        vaccine_severe_disease_reduction: 0.88
    }
};

/**
 * Pseudo-random Laplace Noise Generator for Differential Privacy
 */
function sampleLaplace(loc, scale) {
    const u = Math.random() - 0.5;
    return loc - scale * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
}

/**
 * Gini Coefficient Calculation
 */
function calculateGini(values, weights) {
    const n = values.length;
    let indexed = values.map((v, i) => ({ val: v, w: weights[i] }));
    indexed.sort((a, b) => a.val - b.val);

    let sumWeights = 0;
    let sumWeightedVals = 0;
    for (let i = 0; i < n; i++) {
        sumWeights += indexed[i].w;
        sumWeightedVals += indexed[i].val * indexed[i].w;
    }
    if (sumWeightedVals === 0) return 0.0;

    let cumW = 0;
    let cumV = 0;
    let area = 0;

    for (let i = 0; i < n; i++) {
        const prevW = cumW;
        const prevV = cumV;
        cumW += indexed[i].w / sumWeights;
        cumV += (indexed[i].val * indexed[i].w) / sumWeightedVals;
        area += (cumW - prevW) * (prevV + cumV) / 2.0;
    }

    const gini = 1.0 - 2.0 * area;
    return Math.max(0.0, Math.min(1.0, gini));
}

/**
 * Four Distributive Justice Allocation Algorithms
 */
const Allocators = {
    // 1. Utilitarian (Bentham / Mill: Maximize Net Survival or QALYs)
    utilitarian: function(resourceType, totalAvailable, cohortStates, clinParams, utilTarget) {
        if (totalAvailable <= 0) return { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };
        
        let marginalGains = {};
        let demands = {};

        for (let c of Object.keys(cohortStates)) {
            let clin = clinParams.cohort_clinical_profiles[c];
            let demand = 0;
            let unitGain = 0;

            if (resourceType === "icu_beds") {
                demand = cohortStates[c].active_critical_demand || 0;
                let deltaCFR = Math.max(0.01, clin.cfr_icu_depleted - clin.cfr_icu_optimal);
                unitGain = (utilTarget === "qalys") ? (deltaCFR * clin.avg_life_years_remaining) : deltaCFR;
            } else {
                demand = cohortStates[c].S || 0;
                let severeRisk = clin.ihr * clin.icu_given_hosp * clin.cfr_icu_depleted;
                unitGain = (utilTarget === "qalys") ? (severeRisk * clin.avg_life_years_remaining) : severeRisk;
            }

            marginalGains[c] = Math.max(1e-4, unitGain);
            demands[c] = Math.max(0, demand);
        }

        let sorted = Object.keys(marginalGains).sort((a, b) => marginalGains[b] - marginalGains[a]);
        let allocations = { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };
        let remaining = totalAvailable;

        for (let c of sorted) {
            let alloc = Math.min(remaining, demands[c]);
            allocations[c] = alloc;
            remaining -= alloc;
            if (remaining <= 0) break;
        }

        if (remaining > 0) {
            let totG = Object.values(marginalGains).reduce((a, b) => a + b, 0);
            for (let c of Object.keys(cohortStates)) {
                allocations[c] += remaining * (marginalGains[c] / totG);
            }
        }
        return allocations;
    },

    // 2. Rawlsian Maximin (John Rawls / Norman Daniels: Prioritize the Worst-Off)
    rawlsian: function(resourceType, totalAvailable, cohortStates, clinParams) {
        if (totalAvailable <= 0) return { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };

        let vulnerability = {};
        let demands = {};

        for (let c of Object.keys(cohortStates)) {
            let clin = clinParams.cohort_clinical_profiles[c];
            let pop = cohortStates[c].N || 1;
            let deaths = cohortStates[c].D || 0;
            let curMort = deaths / pop;

            vulnerability[c] = (clin.cfr_icu_depleted * 2.0) + (curMort * 100.0);
            demands[c] = (resourceType === "icu_beds") ? (cohortStates[c].active_critical_demand || 0) : (cohortStates[c].S || 0);
        }

        let sorted = Object.keys(vulnerability).sort((a, b) => vulnerability[b] - vulnerability[a]);
        let allocations = { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };
        let remaining = totalAvailable;

        for (let c of sorted) {
            let alloc = Math.min(remaining, demands[c]);
            allocations[c] = alloc;
            remaining -= alloc;
            if (remaining <= 0) break;
        }

        if (remaining > 0) {
            let totV = Object.values(vulnerability).reduce((a, b) => a + b, 0);
            for (let c of sorted) {
                allocations[c] += remaining * (vulnerability[c] / totV);
            }
        }
        return allocations;
    },

    // 3. Egalitarian (Strict Per-Capita Demographic Parity)
    egalitarian: function(resourceType, totalAvailable, cohortStates) {
        if (totalAvailable <= 0) return { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };

        let totPop = Object.values(cohortStates).reduce((sum, s) => sum + s.N, 0);
        let allocations = {};
        for (let c of Object.keys(cohortStates)) {
            allocations[c] = totalAvailable * (cohortStates[c].N / totPop);
        }
        return allocations;
    },

    // 4. Privacy-Preserving Surveillance (Laplace Noise under DP Epsilon)
    privacy: function(resourceType, totalAvailable, cohortStates, epsilon) {
        if (totalAvailable <= 0) return { C1_Youth: 0, C2_Informal_Labor: 0, C3_Elderly: 0 };

        let scale = 1.0 / Math.max(0.05, epsilon);
        let noisy = {};

        for (let c of Object.keys(cohortStates)) {
            let raw = (resourceType === "icu_beds") 
                ? (cohortStates[c].active_critical_demand || 0)
                : ((cohortStates[c].I || 0) * 1.2 + (cohortStates[c].S || 0) * 0.1);

            let noise = sampleLaplace(0.0, scale * (raw * 0.12 + 8.0));
            noisy[c] = Math.max(1.0, raw + noise);
        }

        let totNoisy = Object.values(noisy).reduce((a, b) => a + b, 0);
        let allocations = {};
        for (let c of Object.keys(cohortStates)) {
            allocations[c] = totalAvailable * (noisy[c] / totNoisy);
        }
        return allocations;
    }
};

/**
 * Execute Epidemiological Simulation
 */
function runEpidemicSimulation(demoConfig, clinConfig, durationDays, initInfFraction, policyKey, options) {
    const cohortKeys = Object.keys(demoConfig.cohorts);
    const totalPop = demoConfig.total_population;

    const r0 = clinConfig.disease_dynamics.r0_baseline;
    const sigma = 1.0 / clinConfig.disease_dynamics.latent_period_days;
    const gamma = 1.0 / clinConfig.disease_dynamics.infectious_period_days;
    const betaBase = r0 * gamma;

    const icuCapacity = (demoConfig.resources.icu_beds_per_100k / 100000.0) * totalPop;
    const dailyVaccines = demoConfig.resources.daily_vaccine_capacity;

    // History logs
    let history = {
        days: Array.from({ length: durationDays }, (_, i) => i),
        infections: { C1_Youth: [], C2_Informal_Labor: [], C3_Elderly: [] },
        total_infections: [],
        critical_icu: { C1_Youth: [], C2_Informal_Labor: [], C3_Elderly: [] },
        total_critical: [],
        deaths: { C1_Youth: [], C2_Informal_Labor: [], C3_Elderly: [] },
        total_deaths: [],
        unmet_icu_days: [],
        icu_capacity_line: icuCapacity
    };

    // Initialize States
    let state = {};
    for (let c of cohortKeys) {
        let n = demoConfig.cohorts[c].fraction * totalPop;
        let initI = Math.max(5.0, n * initInfFraction * demoConfig.cohorts[c].density_factor);
        state[c] = {
            N: n,
            S: n - initI,
            E: 0.0,
            I: initI,
            R: 0.0,
            C: 0.0,
            D: 0.0,
            active_critical_demand: 0.0
        };
    }

    // Daily Integration Loop
    for (let t = 0; t < durationDays; t++) {
        // Allocate resources
        let allocICU, allocVax;
        if (policyKey === "utilitarian") {
            allocICU = Allocators.utilitarian("icu_beds", icuCapacity, state, clinConfig, options.utilTarget);
            allocVax = Allocators.utilitarian("vaccines", dailyVaccines, state, clinConfig, options.utilTarget);
        } else if (policyKey === "rawlsian") {
            allocICU = Allocators.rawlsian("icu_beds", icuCapacity, state, clinConfig);
            allocVax = Allocators.rawlsian("vaccines", dailyVaccines, state, clinConfig);
        } else if (policyKey === "egalitarian") {
            allocICU = Allocators.egalitarian("icu_beds", icuCapacity, state);
            allocVax = Allocators.egalitarian("vaccines", dailyVaccines, state);
        } else {
            allocICU = Allocators.privacy("icu_beds", icuCapacity, state, options.epsilon);
            allocVax = Allocators.privacy("vaccines", dailyVaccines, state, options.epsilon);
        }

        let dayUnmetICU = 0.0;
        let totalActiveI = cohortKeys.reduce((sum, c) => sum + state[c].I, 0);
        let forceOfInfection = (betaBase * totalActiveI) / totalPop;

        let dayTotalInf = 0;
        let dayTotalCrit = 0;
        let dayTotalDeaths = 0;

        for (let c of cohortKeys) {
            let cData = demoConfig.cohorts[c];
            let cClin = clinConfig.cohort_clinical_profiles[c];

            // Log state
            history.infections[c].push(state[c].I);
            history.critical_icu[c].push(state[c].C);
            history.deaths[c].push(state[c].D);

            dayTotalInf += state[c].I;
            dayTotalCrit += state[c].C;
            dayTotalDeaths += state[c].D;

            // Vaccinations
            let vaxUnits = allocVax[c] || 0;
            let actualVax = Math.min(state[c].S, vaxUnits);
            state[c].S -= actualVax;
            state[c].R += actualVax * clinConfig.intervention_efficacy.vaccine_severe_disease_reduction;

            // SEIR transmission
            let cohortBeta = forceOfInfection * cData.density_factor * cClin.susceptibility_multiplier;
            let newExposed = Math.min(state[c].S, cohortBeta * state[c].S);
            let newInfectious = sigma * state[c].E;

            let hospFraction = cClin.ihr;
            let newHosp = gamma * state[c].I * hospFraction;
            let newMildRecovered = gamma * state[c].I * (1.0 - hospFraction);

            let newCritDemand = newHosp * cClin.icu_given_hosp;
            state[c].active_critical_demand += newCritDemand;

            let assignedBeds = allocICU[c] || 0;
            let admittedICU = Math.min(state[c].active_critical_demand, assignedBeds);
            let unmetCritical = Math.max(0, state[c].active_critical_demand - assignedBeds);
            dayUnmetICU += unmetCritical;

            let critExitRate = 1.0 / clinConfig.disease_dynamics.icu_stay_days;
            let exitingAdmitted = admittedICU * critExitRate;
            let exitingUnmet = unmetCritical * critExitRate;

            let dailyDeaths = (exitingAdmitted * cClin.cfr_icu_optimal) + (exitingUnmet * cClin.cfr_icu_depleted);
            let dailyCritRecovered = (exitingAdmitted * (1.0 - cClin.cfr_icu_optimal)) + (exitingUnmet * (1.0 - cClin.cfr_icu_depleted));

            // Compartment transitions
            state[c].S = Math.max(0, state[c].S - newExposed);
            state[c].E = Math.max(0, state[c].E + newExposed - newInfectious);
            state[c].I = Math.max(0, state[c].I + newInfectious - (newMildRecovered + newHosp));
            state[c].C = admittedICU;
            state[c].active_critical_demand = Math.max(0, state[c].active_critical_demand - (exitingAdmitted + exitingUnmet));
            state[c].R += newMildRecovered + dailyCritRecovered;
            state[c].D += dailyDeaths;
        }

        history.total_infections.push(dayTotalInf);
        history.total_critical.push(dayTotalCrit);
        history.total_deaths.push(dayTotalDeaths);
        history.unmet_icu_days.push(dayUnmetICU);
    }

    // Compute Summary Metrics
    let finalDeaths = {};
    let mortRates = [];
    let popWeights = [];
    let qalysLost = 0;

    for (let c of cohortKeys) {
        let d = state[c].D;
        let n = state[c].N;
        finalDeaths[c] = Math.round(d * 10) / 10;
        mortRates.push(d / n);
        popWeights.push(n);
        qalysLost += d * clinConfig.cohort_clinical_profiles[c].avg_life_years_remaining;
    }

    let totDeaths = Object.values(finalDeaths).reduce((a, b) => a + b, 0);
    let mortGini = calculateGini(mortRates, popWeights);
    let minRate = Math.min(...mortRates.filter(r => r > 0));
    let maxRate = Math.max(...mortRates);
    let disparityRatio = minRate > 0 ? (maxRate / minRate) : 1.0;
    let totUnmetICUDays = history.unmet_icu_days.reduce((a, b) => a + b, 0);

    return {
        history: history,
        metrics: {
            total_deaths: Math.round(totDeaths),
            total_qalys_lost: Math.round(qalysLost),
            mortality_gini: Math.round(mortGini * 10000) / 10000,
            disparity_ratio: Math.round(disparityRatio * 10) / 10,
            total_unmet_icu_days: Math.round(totUnmetICUDays),
            cohort_deaths: finalDeaths,
            cohort_mort_pct: {
                C1_Youth: Math.round((finalDeaths.C1_Youth / (demoConfig.cohorts.C1_Youth.fraction * totalPop)) * 10000) / 100,
                C2_Informal_Labor: Math.round((finalDeaths.C2_Informal_Labor / (demoConfig.cohorts.C2_Informal_Labor.fraction * totalPop)) * 10000) / 100,
                C3_Elderly: Math.round((finalDeaths.C3_Elderly / (demoConfig.cohorts.C3_Elderly.fraction * totalPop)) * 10000) / 100
            }
        }
    };
}
