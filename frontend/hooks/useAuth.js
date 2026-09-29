import { useState, useEffect, useCallback } from "react";
import { API_TOKEN_KEY, API_REFRESH_MS, apiFetchMe, apiLogout } from "../services/api/client.js";
import { safeUser, storeSession, clearSession } from "../services/auth/authService.js";
import { normalizeCompetencyPayload } from "../services/competency/competencyEngine.js";

export function useAuth(onSnapshotApplied) {
  const [user, setUser] = useState(() => safeUser());
  const [profileData, setProfileData] = useState(null);
  const [apiToken, setApiToken] = useState(() => (typeof localStorage !== "undefined" ? localStorage.getItem(API_TOKEN_KEY) || "" : ""));
  const [loggedIn, setLoggedIn] = useState(() => Boolean(typeof localStorage !== "undefined" && localStorage.getItem(API_TOKEN_KEY)));

  const applyApiSnapshot = useCallback((snapshot) => {
    const data = snapshot?.data || snapshot;
    if (!data) return;
    const normalized = normalizeCompetencyPayload(data);
    setProfileData(data);
    const currentUser = data.user || data.profile || null;
    setUser(currentUser);
    if (currentUser) {
      localStorage.setItem("statSkillUser", JSON.stringify(currentUser));
    }
    if (onSnapshotApplied) {
      onSnapshotApplied(normalized);
    }
  }, [onSnapshotApplied]);

  // Session refresh & window focus listener
  useEffect(() => {
    if (!loggedIn || !apiToken) return undefined;

    let mounted = true;
    const refreshUserData = async () => {
      try {
        const snapshot = await apiFetchMe(apiToken);
        if (mounted) applyApiSnapshot(snapshot);
      } catch (error) {
        console.warn("Unable to refresh user data:", error);
        if (mounted && /401|session|token/i.test(String(error.message || ""))) {
          clearSession();
          setApiToken("");
          setLoggedIn(false);
        }
      }
    };

    refreshUserData();
    const intervalId = window.setInterval(refreshUserData, API_REFRESH_MS);
    const handleFocus = () => refreshUserData();
    window.addEventListener("focus", handleFocus);

    const handleUnauthorized = () => {
      clearSession();
      setApiToken("");
      setLoggedIn(false);
    };
    window.addEventListener("statskill:unauthorized", handleUnauthorized);

    return () => {
      mounted = false;
      window.clearInterval(intervalId);
      window.removeEventListener("focus", handleFocus);
      window.removeEventListener("statskill:unauthorized", handleUnauthorized);
    };
  }, [loggedIn, apiToken, applyApiSnapshot]);

  const login = (sessionData) => {
    storeSession(sessionData);
    const token = sessionData.access_token || "";
    setApiToken(token);
    setLoggedIn(true);
    applyApiSnapshot(sessionData.data || sessionData);
  };

  const logout = async () => {
    if (apiToken) {
      await apiLogout(apiToken);
    }
    clearSession();
    setApiToken("");
    setLoggedIn(false);
    setUser(safeUser());
    setProfileData(null);
  };

  return {
    user,
    setUser,
    apiToken,
    loggedIn,
    profileData,
    login,
    logout,
    applyApiSnapshot,
  };
}
