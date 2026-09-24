import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.1-flash-lite"

def check_domain(paper_text: str) -> bool:
    """
    Quick check: is this an IT/Computer Science paper?
    Returns True if likely IT-related, False otherwise.
    """
    prompt = f"""You are a strict classifier. Read the excerpt below and answer with ONLY one word: "YES" or "NO".
Question: Is this text from an IT / Computer Science academic paper (e.g. software engineering, AI, networks, databases, algorithms)?

Excerpt:
\"\"\"{paper_text[:1500]}\"\"\"

Answer:"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    answer = response.text.strip().upper()
    return answer.startswith("YES")


def simplify_paper(paper_text: str) -> dict:
    """
    Sends the paper text to Gemini and returns a dict with:
      - sections: list of {heading, original, simplified}
      - glossary: list of {term, definition}
    Math/algorithms are explicitly left untouched.
    """
    prompt = f"""You are an assistant that helps bachelor-level IT students understand academic papers.

Rules:
1. SIMPLIFIED: Rewrite the paper's prose in plain, simple English for a bachelor-level IT student. Remove jargon, passive voice, and unnecessary complexity. Add brief background context only where it's needed to understand the point — don't pad. Use a simple analogy whenever you think it's handfull.
2. ORIGINAL: Also return a condensed version of the original text for this section — trim to roughly 60-70% of its original length by cutting redundant phrasing and filler, but keep the real wording, sentence style, and all key claims/numbers intact. Do NOT rewrite it in your own words and do NOT compress it down to just a sentence or two — it must stay clearly longer and denser than the simplified version, so the difference between the two is obvious.
3. STRUCTURE: Preserve the paper's real section headings, in order. Do not invent, merge, or skip sections.
4. MATH: Never simplify, solve, translate, or explain equations, formulas, proofs, or algorithms. Copy them exactly in both "original" and "simplified", or write "[technical content unchanged]" in "simplified" only if omitting a block for length.
5. GLOSSARY: Extract only the 10-15 most important/unfamiliar terms central to this specific paper. Skip terms a CS bachelor student already knows (function, database, algorithm, variable, etc). Each term appears once; if a term repeats across sections, only define it the first time.
6. ACCURACY: Never change factual meaning, numbers, or claims. If a claim is ambiguous, keep it close to the source wording rather than guessing or inventing detail.
7. OUTPUT: Return ONLY valid JSON, no markdown fences, no commentary, matching the schema exactly — every section must have "heading", "original", and "simplified" as non-empty strings.

Return ONLY valid JSON in this exact format, no markdown, no extra text:
{{
  "sections": [
    {{"heading": "...", "original": "...", "simplified": "..."}}
  ],
  "glossary": [
    {{"term": "...", "definition": "..."}}
  ]
}}

Paper text:
\"\"\"{paper_text}\"\"\"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json\n", "", 1).replace("json", "", 1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw[:500]}")

    return data