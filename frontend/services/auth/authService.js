import { API_TOKEN_KEY } from "../api/client.js";

const USER_KEY = "statSkillUser";

export function safeUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY) || "null");
  } catch {
    return null;
  }
}

export function getStoredToken() {
  return localStorage.getItem(API_TOKEN_KEY) || "";
}

export function isAuthenticated() {
  return Boolean(getStoredToken());
}

export function storeSession(token, user) {
  if (token) localStorage.setItem(API_TOKEN_KEY, token);
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearSession() {
  localStorage.removeItem(API_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem("statSkillSession");
}

export function isOfficerUser(user) {
  if (!user) return false;
  const accountType = String(user.accountType || user.account_type || "").toLowerCase();
  return accountType === "cadre_officer" || accountType === "officer" || accountType.includes("officer");
}
