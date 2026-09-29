import {
  BarChart3,
  FileText,
  ShieldCheck,
  Target,
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
    name: "Statistical Methods",
    icon: BarChart3,
    benchmark: 3.5,
    weight: 1.15,
    description: "Inference, sampling, regression and time-series analysis.",
    subSkills: [
      "Descriptive Statistics",
      "Hypothesis Testing",
      "Regression Analysis",
      "Time Series Analysis",
    ],
  },
  {
    key: "dataQuality",
    name: "Data Quality",
    icon: ShieldCheck,
    benchmark: 3.5,
    weight: 1.05,
    description: "Validation, error detection, review and quality assurance.",
    subSkills: [
      "Data Validation",
      "Error Detection",
      "Imputation",
      "Audit & Review",
    ],
  },
  {
    key: "python",
    name: "Python",
    icon: FileText,
    benchmark: 3,
    weight: 1,
    description: "Python for data analysis, automation and statistical workflows.",
    subSkills: ["pandas", "Visualisation", "Automation", "Statistical Libraries"],
  },
  {
    key: "gis",
    name: "GIS & Spatial Statistics",
    icon: Target,
    benchmark: 3,
    weight: 1,
    description: "Spatial datasets, mapping, GIS tools and geographic analysis.",
    subSkills: [
      "Map Projections",
      "Spatial Joins",
      "GIS Tools",
      "Choropleth Mapping",
    ],
  },
  {
    key: "machineLearning",
    name: "Machine Learning",
    icon: Zap,
    benchmark: 3,
    weight: 0.95,
    description: "Predictive modelling, evaluation and feature engineering.",
    subSkills: [
      "Supervised Learning",
      "Model Evaluation",
      "Feature Engineering",
      "ML Frameworks",
    ],
  },
];

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

export function runCompetencyEngine(data = KARMAYOGI_DATA) {
  const normalized = normalizeCompetencyPayload(data);

  const competencies = ENGINE_DEFINITIONS.map((def) => {
    const supplied = Array.isArray(normalized.competencies)
      ? normalized.competencies.find(
          (item) => (item.key || item.id) === def.key
        )
      : null;

    const assessments = normalized.assessments.filter(
      (item) => item.domain === def.key
    );
    const courses = normalized.courses.filter((item) => item.domain === def.key);
    const self = average(normalized.selfAssessment?.[def.key] || []);
    const hours = Number(normalized.learningHours?.[def.key] || 0);

    const quiz = average(assessments.map((item) => item.score)) / 20;
    const course = average(courses.map((item) => item.score)) / 20;
    const effort = Math.min(5, hours / 8);

    const calculatedScore = Math.max(
      0,
      Math.min(5, quiz * 0.5 + course * 0.25 + self * 0.15 + effort * 0.1)
    );

    const suppliedScore = Number(
      normalized.competencyScores?.[def.key] ??
        supplied?.scoreOutOf5 ??
        supplied?.score
    );

    const score = Number.isFinite(suppliedScore)
      ? Math.max(0, Math.min(5, suppliedScore))
      : calculatedScore;

    const level =
      supplied?.level || (score >= 3.5 ? "Strong" : score >= 2 ? "Moderate" : "Weak");
    const benchmark = Number(supplied?.benchmark ?? def.benchmark);
    const gap = Math.max(0, benchmark - score);

    let trend = supplied?.trend || "Stable";
    if (!supplied?.trend && assessments.length > 1) {
      const delta =
        Number(assessments[assessments.length - 1]?.score || 0) -
        Number(assessments[0]?.score || 0);
      trend = delta >= 5 ? "Improving" : delta <= -5 ? "Declining" : "Stable";
    }

    return {
      ...def,
      ...(supplied || {}),
      key: def.key,
      name: supplied?.name || def.name,
      score: Number(score.toFixed(2)),
      scoreOutOf5: Number(score.toFixed(2)),
      scorePercent: Number((score * 20).toFixed(1)),
      benchmark,
      level,
      trend,
      gap: Number(gap.toFixed(2)),
      gapPercent: benchmark ? Number(((gap / benchmark) * 100).toFixed(1)) : 0,
      weight: Number(supplied?.weight ?? def.weight),
      evidence: supplied?.evidence || {
        quizAverage: Math.round(average(assessments.map((item) => item.score))),
        courseAverage: Math.round(average(courses.map((item) => item.score))),
        selfAssessment: Math.round(self * 20),
        learningHours: hours,
      },
      subSkills: supplied?.subSkills?.length
        ? supplied.subSkills
        : def.subSkills.map((name, i) => ({
            name,
            score: Math.round(
              Number((normalized.selfAssessment?.[def.key] || [])[i] || 0) * 20
            ),
          })),
    };
  });

  const totalWeight =
    competencies.reduce((sum, item) => sum + Number(item.weight || 1), 0) || 1;
  const weighted =
    competencies.reduce(
      (sum, item) => sum + item.score * Number(item.weight || 1),
      0
    ) / totalWeight;
  const quizAverage = Math.round(
    average(normalized.assessments.map((item) => item.score))
  );
  const totalHours = Object.values(normalized.learningHours || {}).reduce(
    (sum, value) => sum + Number(value || 0),
    0
  );

  const sourceDashboard = normalized.dashboard || {};
  const overallScore = Number.isFinite(Number(sourceDashboard.overallCompetency))
    ? Number(sourceDashboard.overallCompetency)
    : Math.round(
        Math.min(
          100,
          Math.max(
            0,
            weighted * 20 * 0.82 +
              quizAverage * 0.12 +
              Math.min(totalHours, 100) * 0.06
          )
        )
      );

  const topGaps =
    Array.isArray(normalized.criticalSkills) && normalized.criticalSkills.length
      ? normalized.criticalSkills
          .map(
            (item) =>
              competencies.find(
                (c) => c.name === item.competency || c.key === item.competency
              ) || item
          )
          .slice(0, 3)
      : [...competencies].sort((a, b) => b.gap - a.gap).slice(0, 3);

  const fallbackRecommendations = {
    gis: "Complete GIS for Statistics and practise spatial joins and choropleth mapping.",
    machineLearning:
      "Strengthen Python foundations before moving into model evaluation and ML.",
    python:
      "Build pandas, visualisation and automation skills through practical datasets.",
    dataQuality:
      "Practise validation, error detection and statistical audit workflows.",
    statisticalMethods:
      "Target sampling, regression and time-series exercises for greater analytical depth.",
  };

  const recommendations = Array.isArray(normalized.recommendations)
    ? normalized.recommendations
    : topGaps
        .map(
          (item) =>
            normalized.criticalSkills?.find((cs) => cs.competency === item.name)
              ?.recommendedAction || fallbackRecommendations[item.key]
        )
        .filter(Boolean);

  const moduleList = normalized.modules || [];
  const completedModules = Number(
    normalized.learningPath?.modulesCompleted ??
      sourceDashboard.completedModules ??
      moduleList.filter((m) => String(m.status || "").toLowerCase() === "completed")
        .length
  );

  const totalModules = Number(
    normalized.learningPath?.totalModules ??
      sourceDashboard.totalModules ??
      moduleList.length
  );

  const learningProgress = Number(
    sourceDashboard.learningProgress ??
      (normalized.learningPath?.modulesCompleted != null &&
      normalized.learningPath?.totalModules
        ? Math.round(
            (Number(normalized.learningPath.modulesCompleted) /
              Number(normalized.learningPath.totalModules)) *
              100
          )
        : average(moduleList.map((m) => Number(m.progress || 0))))
  );

  const assessmentsCompleted = Number(
    sourceDashboard.assessmentsCompleted ??
      normalized.assessments.filter(
        (item) => String(item.status || "Completed").toLowerCase() === "completed"
      ).length
  );
  const assessmentsTotal = Number(
    sourceDashboard.assessmentsTotal ?? normalized.assessments.length
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
    assessmentAverage: Number(sourceDashboard.assessmentAverage ?? quizAverage),
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
      normalized.dashboard?.assignmentsCompleted ??
        normalized.assignments.filter(
          (item) => String(item.status || "").toLowerCase() === "completed"
        ).length
    ),
    assignmentsTotal: Number(
      normalized.dashboard?.assignmentsTotal ?? normalized.assignments.length
    ),
    coursesCompleted: Number(
      normalized.dashboard?.coursesCompleted ??
        normalized.courses.filter(
          (item) => String(item.status || "").toLowerCase() === "completed"
        ).length
    ),
    coursesTotal: normalized.courses.length,
    rank: normalized.dashboard?.rank || "A",
    level: Number(normalized.dashboard?.level ?? overallScore),
    xp: Number(normalized.dashboard?.xp ?? 0),
    methodology:
      normalized.engine?.methodology ||
      "50% assessments · 25% courses · 15% self-assessment · 10% learning effort",
  };
}
