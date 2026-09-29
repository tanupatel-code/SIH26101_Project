"""
StatSkill AI — AI MCQ Provider Abstraction Layer.
Defines unified provider interface, cloud adapters (Gemini & OpenAI), and deterministic local fallback.
"""

from __future__ import annotations

import abc
import json
import logging
import os
import re
from typing import Any

logger = logging.getLogger("statskill.mcq_providers")


class BaseMCQProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        """Name of the MCQ generation provider."""
        pass

    @abc.abstractmethod
    def generate(
        self,
        text: str,
        num_questions: int,
        difficulty: str,
        bloom_level: str,
        domain: str | None,
    ) -> list[dict[str, Any]] | None:
        """Generates raw candidate questions."""
        pass


class GeminiMCQProvider(BaseMCQProvider):
    @property
    def provider_name(self) -> str:
        return "gemini"

    def generate(
        self,
        text: str,
        num_questions: int,
        difficulty: str,
        bloom_level: str,
        domain: str | None,
    ) -> list[dict[str, Any]] | None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None

        prompt = f"""
You are an expert psychometrician and statistical education designer for India's Official Statistical System (MoSPI/NSSTA).
Generate exactly {num_questions} multiple-choice questions based on the following learning material.
Difficulty Level: {difficulty}
Bloom's Taxonomy Level: {bloom_level}
Target Competency Domain: {domain or 'Official Statistics'}

LEARNING MATERIAL:
{text[:4000]}

Format output as a valid JSON array of objects with keys:
- "question": string
- "topic": string
- "options": list of exactly 4 strings
- "correct_index": integer (0, 1, 2, or 3)
- "bloom_level": string
- "domain": string
- "explanation": string (clear educational rationale for the correct answer)
"""
        try:
            import httpx

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"},
            }
            # Timeout guard: 15 seconds
            res = httpx.post(url, json=payload, timeout=15.0)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_text)
                if isinstance(parsed, list):
                    return parsed
        except Exception as exc:
            # Safe logging: never leak the API key
            logger.warning("Gemini generation failed (%s), falling back to local engine.", type(exc).__name__)

        return None


class OpenAIMCQProvider(BaseMCQProvider):
    @property
    def provider_name(self) -> str:
        return "openai"

    def generate(
        self,
        text: str,
        num_questions: int,
        difficulty: str,
        bloom_level: str,
        domain: str | None,
    ) -> list[dict[str, Any]] | None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        prompt = f"""
You are an expert psychometrician and statistical education designer for India's Official Statistical System (MoSPI/NSSTA).
Generate exactly {num_questions} multiple-choice questions based on the following learning material.
Difficulty Level: {difficulty}
Bloom's Taxonomy Level: {bloom_level}
Target Competency Domain: {domain or 'Official Statistics'}

LEARNING MATERIAL:
{text[:4000]}

Format output as a valid JSON array of objects with keys:
- "question": string
- "topic": string
- "options": list of exactly 4 strings
- "correct_index": integer (0, 1, 2, or 3)
- "bloom_level": string
- "domain": string
- "explanation": string (clear educational rationale for the correct answer)
"""
        try:
            import httpx

            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
            }
            # Timeout guard: 15 seconds
            res = httpx.post(url, json=payload, headers=headers, timeout=15.0)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["choices"][0]["message"]["content"]
                parsed = json.loads(raw_text)
                if isinstance(parsed, dict) and "questions" in parsed:
                    return parsed["questions"]
                elif isinstance(parsed, list):
                    return parsed
        except Exception as exc:
            # Safe logging: never leak the API key
            logger.warning("OpenAI generation failed (%s), falling back to local engine.", type(exc).__name__)

        return None


class LocalMCQProvider(BaseMCQProvider):
    @property
    def provider_name(self) -> str:
        return "local"

    def generate(
        self,
        text: str,
        num_questions: int,
        difficulty: str,
        bloom_level: str,
        domain: str | None,
    ) -> list[dict[str, Any]] | None:
        from services.mcq_generator import (
            OFFICIAL_STATS_CONCEPTS,
            extract_keywords_from_text,
            generate_document_specific_mcqs,
        )

        extracted_terms = extract_keywords_from_text(text) if text else []
        pool = list(OFFICIAL_STATS_CONCEPTS)

        if domain:
            matched = [q for q in pool if q.get("domain") == domain]
            if matched:
                pool = matched

        if extracted_terms:
            def relevance_score(q: dict[str, Any]) -> int:
                q_text = (q["question"] + " " + q.get("topic", "")).lower()
                return sum(1 for term in extracted_terms if term in q_text)

            pool = sorted(pool, key=relevance_score, reverse=True)

        custom_doc_mcqs = generate_document_specific_mcqs(text, difficulty, bloom_level, domain)
        combined_pool = custom_doc_mcqs + pool

        raw_candidates: list[dict[str, Any]] = []
        seen_texts: set[str] = set()

        for item in combined_pool:
            q_text = item["question"]
            if q_text in seen_texts:
                continue
            seen_texts.add(q_text)

            q_copy = dict(item)
            q_copy["difficulty"] = difficulty
            q_copy["bloom_level"] = bloom_level if bloom_level else q_copy.get("bloom_level", "Understanding")
            raw_candidates.append(q_copy)

            if len(raw_candidates) >= num_questions:
                break

        # If more questions needed, derive variants from pool
        while len(raw_candidates) < num_questions and pool:
            base = pool[len(raw_candidates) % len(pool)]
            cloned = dict(base)
            cloned["difficulty"] = difficulty
            cloned["bloom_level"] = bloom_level if bloom_level else cloned.get("bloom_level", "Understanding")
            cloned["question"] = f"{base['question']} (Analytical Variant #{len(raw_candidates) + 1})"
            raw_candidates.append(cloned)

        return raw_candidates

    def generate_mcqs(
        self,
        text: str,
        domain: str | None = None,
        difficulty: str = "Intermediate",
        count: int = 5,
        bloom_level: str = "Understanding",
    ) -> list[dict[str, Any]]:
        raw = self.generate(text, num_questions=count, difficulty=difficulty, bloom_level=bloom_level, domain=domain) or []
        from services.mcq_generator import validate_and_sanitize_mcqs
        validated = validate_and_sanitize_mcqs(raw, target_domain=domain, difficulty=difficulty, bloom_level=bloom_level)
        for q in validated:
            q["_provider"] = "local_rule_based"
        return validated


class CompositeMCQProvider:
    """
    Coordinates provider resolution:
    Checks for configured cloud providers (Gemini / OpenAI), attempts generation,
    and falls back to LocalMCQProvider if cloud generation fails or is unconfigured.
    """

    def __init__(self) -> None:
        self.gemini = GeminiMCQProvider()
        self.openai = OpenAIMCQProvider()
        self.local = LocalMCQProvider()

    def generate(
        self,
        text: str,
        num_questions: int = 5,
        difficulty: str = "Intermediate",
        bloom_level: str = "Understanding",
        domain: str | None = None,
    ) -> tuple[list[dict[str, Any]], str]:
        # 1. Try Gemini if configured
        if os.getenv("GEMINI_API_KEY"):
            results = self.gemini.generate(text, num_questions, difficulty, bloom_level, domain)
            if results and len(results) >= 1:
                return results, "gemini"

        # 2. Try OpenAI if configured
        if os.getenv("OPENAI_API_KEY"):
            results = self.openai.generate(text, num_questions, difficulty, bloom_level, domain)
            if results and len(results) >= 1:
                return results, "openai"

        # 3. Deterministic Local Statistical Provider
        local_results = self.local.generate(text, num_questions, difficulty, bloom_level, domain) or []
        return local_results, "local"

    def generate_mcqs(
        self,
        text: str,
        domain: str | None = None,
        difficulty: str = "Intermediate",
        count: int = 5,
        bloom_level: str = "Understanding",
    ) -> list[dict[str, Any]]:
        raw, provider_used = self.generate(text, num_questions=count, difficulty=difficulty, bloom_level=bloom_level, domain=domain)
        from services.mcq_generator import validate_and_sanitize_mcqs
        validated = validate_and_sanitize_mcqs(raw, target_domain=domain, difficulty=difficulty, bloom_level=bloom_level)
        for q in validated:
            q["_provider"] = provider_used
        return validated


composite_mcq_provider = CompositeMCQProvider()
