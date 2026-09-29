import {
  BarChart3,
  FileText,
  Landmark,
  ShieldCheck,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";

export const KARMAYOGI_DATA = {
  competencyScores: {},
  assessments: [],
  courses: [],
  selfAssessment: {},
  learningHours: {},
  modules: [],
  documents: [],
  certificates: [],
  notifications: [],
};

export const ENGINE_DEFINITIONS = [
  {
    key: "statisticalMethods",
    name: "Statistical Methods & Sampling",
    icon: BarChart3,
    benchmark: 3.5,
    weight: 1.15,
    color: "cyan",
    description: "Inference, stratified sampling, variance estimation and hypothesis testing.",
    subSkills: [
      "Sampling Design & Weights",
      "Hypothesis Testing & Inference",
      "Variance Estimation & Standard Errors",
      "Survey Stratification",
    ],
  },
  {
    key: "nationalAccounts",
    name: "National Accounts (SNA & GDP)",
    icon: Landmark,
    benchmark: 3.5,
    weight: 1.10,
    color: "blue",
    description: "System of National Accounts (SNA 2008), GVA vs GDP, and macroeconomic balances.",
    subSkills: [
      "GVA at Basic Prices",
      "GDP at Market Prices",
      "Supply & Use Tables (SUT)",
      "Institutional Sector Accounts",
    ],
  },
  {
    key: "priceIndices",
    name: "Price Statistics (CPI/WPI/IIP)",
    icon: TrendingUp,
    benchmark: 3.5,
    weight: 1.05,
    color: "amber",
    description: "CPI and WPI compilation, Laspeyres weighting, inflation deflators, and basket updates.",
    subSkills: [
      "CPI & WPI Compilation",
      "Modified Laspeyres Formula",
      "Inflation Deflators & Item Weights",
      "Index Quality Adjustment",
    ],
  },
  {
    key: "dataQuality",
    name: "Data Quality & Survey Validation",
    icon: ShieldCheck,
    benchmark: 3.5,
    weight: 1.05,
    color: "green",
    description: "Microdata validation, error detection, hot-deck imputation and audit protocols.",
    subSkills: [
      "Field Data Editing & Validation",
      "Hot-Deck & Cold-Deck Imputation",
      "Microdata Audit & Outlier Detection",
      "Data Quality Review & Standards",
    ],
  },
  {
    key: "gis",
    name: "GIS & Spatial Statistics",
    icon: Target,
    benchmark: 3.0,
    weight: 1.0,
    color: "purple",
    description: "Spatial datasets, Bhuvan geo-tagging, Moran's I and choropleth mapping.",
    subSkills: [
      "Bhuvan & Geo-tagging",
      "Spatial Autocorrelation & Moran's I",
      "Choropleth Mapping",
      "Urban Frame Survey (UFS) Boundaries",
    ],
  },
  {
    key: "python",
    name: "Python for Data Automation",
    icon: FileText,
    benchmark: 3.0,
    weight: 1.0,
    color: "green",
    description: "Python scripting, pandas tabulation, workflow automation and validation pipelines.",
    subSkills: [
      "Data Extraction & Cleaning",
      "pandas & numpy Tabulation",
      "Automated Reporting & Validation",
      "Statistical Script Optimization",
    ],
  },
  {
    key: "machineLearning",
    name: "Machine Learning & AI",
    icon: Zap,
    benchmark: 3.0,
    weight: 0.95,
    color: "red",
    description: "Predictive modelling, time-series forecasting, and ethical AI in governance.",
    subSkills: [
      "Supervised Learning for Official Statistics",
      "Time-Series Forecasting & Nowcasting",
      "Feature Engineering & Preprocessing",
      "Model Evaluation & Bias Auditing",
    ],
  },
];

const DEFINITION_MAP = Object.fromEntries(
  ENGINE_DEFINITIONS.map((def) => [def.key, def])
);

export const average = (values) => {
  if (!Array.isArray(values)) return 0;
  const n = values.map(Number).filter(Number.isFinite);
  return n.length ? n.reduce((a, b) => a + b, 0) / n.length : 0;
};

export function normalizeCompetencyPayload(payload) {
  const source =
    payload?.data && typeof payload.data === "object"
      ? payload.data
      : payload || {};
  const apiUser = source.user || source.profile || {};
  const profile = source.profile || apiUser;

  const scoreMap = { ...(source.competencyScores || {}) };

  if (Array.isArray(source.competencies)) {
    source.competencies.forEach((item) => {
      const key = item?.key || item?.id;
      const score = Number(item?.score ?? item?.scoreOutOf5);
      if (key && Number.isFinite(score)) scoreMap[key] = score;
    });
  }

  const assessmentHistory = Array.isArray(source.assessmentHistory)
    ? source.assessmentHistory
    : Array.isArray(source.assessments)
      ? source.assessments
      : [];

  const assessments = assessmentHistory.map((item) => ({
    ...item,
    title: item.title || item.assessment || "Assessment",
    score: Number(item.score ?? 0),
  }));

  const modules = Array.isArray(source.modules)
    ? source.modules
    : Array.isArray(source.learningPath?.modules)
      ? source.learningPath.modules
      : [];

  const courses = Array.isArray(source.courses) ? source.courses : [];
  const assignments = Array.isArray(source.assignments) ? source.assignments : [];

  const selfAssessment =
    source.selfAssessment || source.rawInputs?.selfAssessment || {};

  const learningHours =
    source.learningHours ||
    source.rawInputs?.learningHours ||
    source.analytics?.learningMixHours ||
    {};

  return {
    ...source,
    user: apiUser,
    profile,
    employeeCode: source.employeeCode || apiUser.employeeCode,
    competencies: Array.isArray(source.competencies) ? source.competencies : [],
    criticalSkills: Array.isArray(source.criticalSkills) ? source.criticalSkills : [],
    benchmarkComparison: Array.isArray(source.benchmarkComparison) ? source.benchmarkComparison : [],
    competencyScores: scoreMap,
    assessments,
    assessmentHistory: assessments,
    assignments,
    courses,
    selfAssessment,
    learningHours,
    modules,
    learningPath: source.learningPath || { modules },
    documents: Array.isArray(source.documents) ? source.documents : [],
    certificates: Array.isArray(source.certificates) ? source.certificates : [],
    notifications: Array.isArray(source.notifications) ? source.notifications : [],
  };
}

/**
 * Authoritative Client Competency Adapter:
 * Uses the backend as the single source of truth for scores, benchmarks, gaps,
 * and readiness levels, enriching items with presentation metadata (Icons, Colors).
 */
export function runCompetencyEngine(data = KARMAYOGI_DATA) {
  const normalized = normalizeCompetencyPayload(data);
  const sourceDashboard = normalized.dashboard || {};

  // Build competencies using authoritative backend values if present, else fallback
  let competencies = [];

  if (Array.isArray(normalized.competencies) && normalized.competencies.length > 0) {
    competencies = normalized.competencies.map((backendItem) => {
      const def = DEFINITION_MAP[backendItem.key] || {};
      const score = Number(backendItem.score ?? backendItem.scoreOutOf5 ?? 2.5);
      const benchmark = Number(backendItem.benchmark ?? def.benchmark ?? 3.5);
      const gap = Number(backendItem.gap ?? Math.max(0, benchmark - score));
      const level =
        backendItem.level ||
        (score >= 3.5 ? "Strong" : score >= 2.0 ? "Moderate" : "Weak");

      const subSkills = Array.isArray(backendItem.subSkills) && backendItem.subSkills.length
        ? (typeof backendItem.subSkills[0] === "string"
            ? backendItem.subSkills.map((name) => ({ name, score: Math.round(score * 20) }))
            : backendItem.subSkills)
        : (def.subSkills || []).map((name) => ({ name, score: Math.round(score * 20) }));

      return {
        ...def,
        ...backendItem,
        icon: def.icon || BarChart3,
        color: backendItem.color || def.color || "cyan",
        score: Number(score.toFixed(2)),
        scoreOutOf5: Number(score.toFixed(2)),
        scorePercent: Number((score * 20).toFixed(1)),
        benchmark,
        gap: Number(gap.toFixed(2)),
        gapPercent: benchmark ? Number(((gap / benchmark) * 100).toFixed(1)) : 0,
        level,
        trend: backendItem.trend || "Stable",
        source: backendItem.source || "authoritative_backend",
        evidence: backendItem.evidence || {
          quizAverage: Math.round(score * 20),
          courseAverage: Math.round(score * 20),
          selfAssessment: Math.round(score * 20),
          learningHours: 0,
        },
        subSkills,
      };
    });
  } else {
    // Fallback: generate default view using ENGINE_DEFINITIONS
    competencies = ENGINE_DEFINITIONS.map((def) => {
      const suppliedScore = Number(normalized.competencyScores?.[def.key]);
      const score = Number.isFinite(suppliedScore) ? suppliedScore : 2.5;
      const benchmark = def.benchmark;
      const gap = Math.max(0, benchmark - score);
      const level = score >= 3.5 ? "Strong" : score >= 2.0 ? "Moderate" : "Weak";

      return {
        ...def,
        score: Number(score.toFixed(2)),
        scoreOutOf5: Number(score.toFixed(2)),
        scorePercent: Number((score * 20).toFixed(1)),
        benchmark,
        level,
        trend: "Stable",
        gap: Number(gap.toFixed(2)),
        gapPercent: benchmark ? Number(((gap / benchmark) * 100).toFixed(1)) : 0,
        evidence: {
          quizAverage: Math.round(score * 20),
          courseAverage: Math.round(score * 20),
          selfAssessment: Math.round(score * 20),
          learningHours: 0,
        },
        subSkills: def.subSkills.map((name) => ({
          name,
          score: Math.round(score * 20),
        })),
      };
    });
  }

  // Dashboard metrics from authoritative backend contract
  const totalWeight =
    competencies.reduce((sum, item) => sum + Number(item.weight || 1), 0) || 1;
  const weightedAvg =
    competencies.reduce((sum, item) => sum + item.score * Number(item.weight || 1), 0) /
    totalWeight;

  const quizAverage = Math.round(
    average(normalized.assessments.map((item) => item.score))
  );
  const totalHours = Object.values(normalized.learningHours || {}).reduce(
    (sum, val) => sum + Number(val || 0),
    0
  );

  const overallScore = Number.isFinite(Number(sourceDashboard.overallCompetency))
    ? Number(sourceDashboard.overallCompetency)
    : Math.round(
        Math.min(
          100,
          Math.max(
            0,
            weightedAvg * 20 * 0.82 +
              quizAverage * 0.12 +
              Math.min(totalHours, 100) * 0.06
          )
        )
      );

  const topGaps =
    Array.isArray(normalized.criticalSkills) && normalized.criticalSkills.length
      ? normalized.criticalSkills
          .map((item) => {
            const comp = competencies.find(
              (c) => c.name === item.competency || c.key === item.key || c.key === item.competency
            );
            return comp ? { ...comp, priority: item.priority } : item;
          })
          .slice(0, 3)
      : [...competencies].sort((a, b) => b.gap - a.gap).slice(0, 3);

  const fallbackRecommendations = {
    statisticalMethods: "Enroll in NSSTA Sampling Techniques & Multi-Stage Survey Design.",
    nationalAccounts: "Review SNA 2008 macroeconomics and GDP compilation methodologies.",
    priceIndices: "Study MoSPI CPI and WPI compilation manuals and Laspeyres index weighting.",
    dataQuality: "Practise validation, field error detection and Hot-Deck statistical imputation.",
    gis: "Complete GIS for Demographics and practise spatial autocorrelation on Bhuvan.",
    python: "Strengthen pandas, visualisation and automation scripts on official datasets.",
    machineLearning: "Study statistical machine learning applications for public policy analytics.",
  };

  const recommendations = Array.isArray(normalized.recommendations) && normalized.recommendations.length
    ? normalized.recommendations
    : topGaps
        .map((item) => {
          const matchedCritical = normalized.criticalSkills?.find(
            (cs) => cs.competency === item.name || cs.key === item.key
          );
          return (
            matchedCritical?.recommendedAction ||
            fallbackRecommendations[item.key] ||
            `Strengthen competencies in ${item.name || item.competency}.`
          );
        })
        .filter(Boolean);

  const moduleList = normalized.modules || [];
  const completedModules = Number(
    normalized.learningPath?.modulesCompleted ??
      sourceDashboard.completedModules ??
      moduleList.filter((m) => String(m.status || "").toLowerCase() === "completed").length
  );

  const totalModules = Number(
    normalized.learningPath?.totalModules ??
      sourceDashboard.totalModules ??
      (moduleList.length || 4)
  );

  const learningProgress = Number(
    sourceDashboard.learningProgress ??
      (totalModules > 0 ? Math.round((completedModules / totalModules) * 100) : 0)
  );

  const assessmentsCompleted = Number(
    sourceDashboard.assessmentsCompleted ??
      normalized.assessments.filter(
        (item) => String(item.status || "Completed").toLowerCase() === "completed"
      ).length
  );
  const assessmentsTotal = Number(
    sourceDashboard.assessmentsTotal ?? Math.max(10, assessmentsCompleted)
  );

  return {
    overallScore,
    criticalGaps: Number(
      sourceDashboard.criticalSkillGaps ??
        competencies.filter((c) => c.level === "Weak").length
    ),
    moderateGaps: Number(
      sourceDashboard.moderateSkillGaps ??
        competencies.filter((c) => c.level === "Moderate").length
    ),
    strongSkills: Number(
      sourceDashboard.strongSkills ??
        competencies.filter((c) => c.level === "Strong").length
    ),
    assessmentAverage: Number(sourceDashboard.assessmentAverage ?? (quizAverage || 70)),
    learningHours: Number(sourceDashboard.learningHours ?? totalHours),
    learningHoursByDomain:
      normalized.analytics?.learningMixHours || {
        ...(normalized.learningHours || {}),
      },
    assessmentHistory: normalized.assessmentHistory,
    competencies,
    topGaps,
    recommendations,
    learningProgress,
    completedModules,
    totalModules,
    assessmentsCompleted,
    assessmentsTotal,
    assignmentsCompleted: Number(
      sourceDashboard.assignmentsCompleted ??
        normalized.assignments.filter(
          (item) => String(item.status || "").toLowerCase() === "completed"
        ).length
    ),
    assignmentsTotal: Number(
      sourceDashboard.assignmentsTotal ?? (normalized.assignments.length || 1)
    ),
    coursesCompleted: Number(
      sourceDashboard.coursesCompleted ??
        normalized.courses.filter(
          (item) => String(item.status || "").toLowerCase() === "completed"
        ).length
    ),
    coursesTotal: normalized.courses.length,
    rank: sourceDashboard.rank || "A",
    level: Number(sourceDashboard.level ?? overallScore),
    xp: Number(sourceDashboard.xp ?? 4000),
    methodology:
      "50% assessments · 25% courses · 15% self-assessment · 10% learning effort (Server-Authoritative)",
  };
}
