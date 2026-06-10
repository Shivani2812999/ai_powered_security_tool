import os
import json
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_report(score: int, level: str, findings: dict) -> dict:

    prompt = f"""
You are a cybersecurity analyst. Analyze the scan results below and return a JSON report.

Risk Score : {score}/100
Risk Level : {level}

Findings:
{json.dumps(findings, indent=2)}

You MUST return ONLY this exact JSON structure with string values:

{{
    "executive_summary": "Write 2-3 sentences summarizing the threat here.",
    "recommendations": "Write numbered recommendations as plain text here. 1. First step. 2. Second step. 3. Third step.",
    "technical_details": "Write a plain text technical breakdown of each API finding here."
}}

STRICT RULES:
- All three values must be plain strings, not arrays or objects
- No markdown, no backticks, no bullet points
- No text before or after the JSON
- Recommendations must be a single string with numbered items inline
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    content = response.choices[0].message.content.strip()

    # strip markdown fences if model adds them
    content = re.sub(r"```json\s*", "", content)
    content = re.sub(r"```\s*",     "", content)
    content = content.strip()

    try:
        parsed = json.loads(content)

        # force all values to strings in case model returns array/object
        return {
            "executive_summary": _to_str(parsed.get("executive_summary", "")),
            "recommendations":   _to_str(parsed.get("recommendations",   "")),
            "technical_details": _to_str(parsed.get("technical_details", "")),
        }

    except Exception:
        # last resort — extract fields with regex
        return {
            "executive_summary": _extract(content, "executive_summary"),
            "recommendations":   _extract(content, "recommendations"),
            "technical_details": _extract(content, "technical_details"),
        }


def _to_str(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(
            f"{i+1}. {item}" if isinstance(item, str)
            else f"{i+1}. {json.dumps(item)}"
            for i, item in enumerate(value)
        )
    if isinstance(value, dict):
        return " | ".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def _extract(text: str, key: str) -> str:
    pattern = rf'"{key}"\s*:\s*"(.*?)"(?=\s*[,}}])'
    match   = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""