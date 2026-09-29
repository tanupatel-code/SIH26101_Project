import { copyEn, dictEn } from "./en.js";
import { copyHi, dictHi } from "./hi.js";
import { copyTa, dictTa } from "./ta.js";
import { copyTe, dictTe } from "./te.js";

export const LOCALIZED_COPY = {
  en: copyEn,
  hi: copyHi,
  ta: copyTa,
  te: copyTe
};

export const DICTIONARY = {
  en: dictEn,
  hi: dictHi,
  ta: dictTa,
  te: dictTe
};

const NOTIFICATIONS = { en: [], hi: [], ta: [], te: [] };

export function notificationsFor(lang) {
  return NOTIFICATIONS[lang] || NOTIFICATIONS.en;
}

export function tr(lang, key) {
  return DICTIONARY[lang]?.[key] || DICTIONARY.en[key] || key;
}

export function copy(lang, key) {
  return LOCALIZED_COPY[lang]?.[key] || LOCALIZED_COPY.en[key] || key;
}
