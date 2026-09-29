import { useState, useEffect } from "react";

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem("statSkillVisualTheme");
    return stored === "executive" || stored === "aurora" || stored === "solo"
      ? stored
      : "executive";
  });
  const [appearance, setAppearance] = useState(
    () => (localStorage.getItem("statSkillAppearance") === "dark" ? "dark" : "light")
  );
  const [lang, setLang] = useState(() =>
    ["en", "hi", "ta", "te"].includes(localStorage.getItem("statSkillLanguage"))
      ? localStorage.getItem("statSkillLanguage")
      : "en"
  );

  useEffect(() => {
    localStorage.setItem("statSkillVisualTheme", theme);
    localStorage.setItem("statSkillAppearance", appearance);
    localStorage.setItem("statSkillLanguage", lang);
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove(
      "theme-solo",
      "theme-executive",
      "theme-aurora",
      "appearance-dark",
      "appearance-light"
    );
    document.body.classList.add(`theme-${theme}`, `appearance-${appearance}`);
  }, [theme, appearance, lang]);

  return {
    theme,
    setTheme,
    appearance,
    setAppearance,
    lang,
    setLang,
  };
}
