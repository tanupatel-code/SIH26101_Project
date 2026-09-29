/**
 * Centralized API Client for StatSkill AI.
 * Handles base URL configuration, Bearer auth headers, error normalization,
 * and unified network requests.
 */

export const API_BASE_URL = (
  (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE_URL) ||
  "http://localhost:8000"
).replace(/\/$/, "");

export const API_TOKEN_KEY = "statSkillApiToken";
export const API_REFRESH_MS = 5000;

export class ApiError extends Error {
  constructor(message, status = 500, details = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

/**
 * Standard fetch wrapper with auth header and error normalization.
 */
export async function apiRequest(endpoint, options = {}) {
  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;
  const headers = {
    Accept: "application/json",
    ...(options.headers || {}),
  };

  const token = options.token || localStorage.getItem(API_TOKEN_KEY);
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }

  // Set JSON Content-Type only if not FormData
  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);
    let payload = null;
    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
      payload = await response.json().catch(() => null);
    } else if (response.ok) {
      return response;
    }

    if (!response.ok) {
      const errorMsg =
        payload?.detail ||
        payload?.message ||
        `HTTP ${response.status}: Request to ${endpoint} failed`;
      throw new ApiError(errorMsg, response.status, payload);
    }

    return payload;
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(err.message || "Network communication failed", 0, err);
  }
}

// ============================================================================
// Auth & User Services
// ============================================================================

export async function apiLogin(email, password) {
  return apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function apiRegister(userData) {
  return apiRequest("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(userData),
  });
}

export async function apiLogout(token) {
  try {
    await apiRequest("/api/auth/logout", {
      method: "POST",
      token,
    });
  } catch {
    // Best-effort session invalidation
  }
}

export async function apiFetchMe(token) {
  return apiRequest("/api/me/data", {
    method: "GET",
    token,
  });
}

export async function apiUpdateProfile(token, profileUpdates) {
  return apiRequest("/api/me/profile", {
    method: "PUT",
    token,
    body: JSON.stringify(profileUpdates),
  });
}

// ============================================================================
// Document Services
// ============================================================================

export async function apiUploadDocument(file, token) {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest("/api/documents/upload", {
    method: "POST",
    token,
    body: formData,
  });
}

export async function apiGetDocuments(token) {
  return apiRequest("/api/documents", {
    method: "GET",
    token,
  });
}

export function getDocumentDownloadUrl(docId) {
  return `${API_BASE_URL}/api/documents/${docId}/download`;
}

// ============================================================================
// Assessment & Quiz Services
// ============================================================================

export async function apiGenerateMCQs(params, token) {
  return apiRequest("/api/mcq/generate", {
    method: "POST",
    token,
    body: JSON.stringify(params),
  });
}

export async function apiGetAvailableAssessments(token) {
  return apiRequest("/api/assessments/available", {
    method: "GET",
    token,
  });
}

export async function apiSubmitAssessment(submission, token) {
  return apiRequest("/api/assessments/submit", {
    method: "POST",
    token,
    body: JSON.stringify(submission),
  });
}

// ============================================================================
// iGOT Services
// ============================================================================

export async function apiGetIgotCourses(domain = null) {
  const query = domain && domain !== "all" ? `?domain=${encodeURIComponent(domain)}` : "";
  return apiRequest(`/api/igot/courses${query}`, { method: "GET" });
}

export async function apiGetIgotRecommendations(token) {
  return apiRequest("/api/igot/recommendations", {
    method: "GET",
    token,
  });
}

export async function apiEnrollIgotCourse(courseId, token) {
  return apiRequest("/api/igot/enroll", {
    method: "POST",
    token,
    body: JSON.stringify({ course_id: courseId }),
  });
}

// ============================================================================
// Reference & Data Sources Services
// ============================================================================

export async function apiGetDataSources() {
  return apiRequest("/api/data-sources", { method: "GET" });
}

export async function apiGetCompetencyFramework() {
  return apiRequest("/api/competencies/framework", { method: "GET" });
}

export function getCertificateDownloadUrl(certId) {
  return `${API_BASE_URL}/api/certificates/${certId}/download`;
}
