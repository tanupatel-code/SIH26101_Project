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
export const API_REFRESH_MS = 60000;

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

  const timeoutMs = options.timeout || 30000;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  const config = {
    ...options,
    headers,
    signal: options.signal || controller.signal,
  };

  try {
    const response = await fetch(url, config);
    clearTimeout(timeoutId);
    let payload = null;
    const contentType = response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
      payload = await response.json().catch(() => null);
    } else if (response.ok) {
      return response;
    }

    if (!response.ok) {
      if (response.status === 401) {
        if (typeof localStorage !== "undefined") {
          localStorage.removeItem(API_TOKEN_KEY);
        }
        if (typeof window !== "undefined") {
          window.dispatchEvent(new CustomEvent("statskill:unauthorized", { detail: payload }));
        }
      }
      const errorMsg =
        payload?.detail ||
        payload?.message ||
        `HTTP ${response.status}: Request to ${endpoint} failed`;
      throw new ApiError(errorMsg, response.status, payload);
    }

    return payload;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      throw new ApiError(`Request timeout after ${timeoutMs}ms for ${endpoint}`, 408);
    }
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

export function getCertificateVerificationUrl(certId) {
  return `${API_BASE_URL}/api/certificates/${certId}/verify`;
}

export async function apiVerifyCertificate(certId) {
  return apiRequest(`/api/certificates/${certId}/verify`, { method: "GET" });
}

export async function apiDownloadCertificateBlob(certId, tokenOrOptions = {}) {
  let token = null;
  let name = null;
  let title = null;

  if (typeof tokenOrOptions === "string") {
    token = tokenOrOptions;
  } else if (tokenOrOptions && typeof tokenOrOptions === "object") {
    token = tokenOrOptions.token;
    name = tokenOrOptions.name;
    title = tokenOrOptions.title;
  }
  if (!token && typeof localStorage !== "undefined") {
    token = localStorage.getItem(API_TOKEN_KEY);
  }

  const params = new URLSearchParams();
  if (name) params.append("name", name);
  if (title) params.append("title", title);
  const query = params.toString() ? `?${params.toString()}` : "";

  const url = `${API_BASE_URL}/api/certificates/${encodeURIComponent(certId)}/download${query}`;
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(url, { headers });
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new ApiError(errorData?.detail || `Certificate download failed: HTTP ${response.status}`, response.status, errorData);
  }
  return response.blob();
}

export async function apiDownloadDocumentBlob(docId, token) {
  const url = `${API_BASE_URL}/api/documents/${docId}/download`;
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(url, { headers });
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new ApiError(errorData?.detail || `Document download failed: HTTP ${response.status}`, response.status, errorData);
  }
  return response.blob();
}
