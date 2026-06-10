import math

from dotenv import load_dotenv
load_dotenv()


def calculate_risk(findings: dict) -> tuple:

    score = 0

    vt      = findings.get("virustotal", {})
    abuse   = findings.get("abuseipdb",  {})
    urlscan = findings.get("urlscan",    {})

    # ── VirusTotal ──────────────────────────────
    malicious     = vt.get("malicious",  0)
    suspicious    = vt.get("suspicious", 0)
    harmless      = vt.get("harmless",   0)
    undetected    = vt.get("undetected", 0)
    total_engines = malicious + suspicious + harmless + undetected or 1
    weighted_bad  = malicious + suspicious * 0.5

    if weighted_bad > 0:
        vt_score = min(70, math.log1p(weighted_bad) / math.log1p(total_engines) * 200)
    else:
        undetected_ratio = undetected / total_engines
        harmless_ratio   = harmless   / total_engines
        uncertainty      = (undetected_ratio * 40) * (1 - harmless_ratio * 0.8)
        vt_score         = min(50, round(uncertainty, 2))

    score += vt_score

    # ── AbuseIPDB ───────────────────────────────
    abuse_score   = abuse.get("abuseConfidenceScore", 0)  # matches your scanner key
    total_reports = abuse.get("totalReports",          0)  # matches your scanner key
    abuse_contrib = (abuse_score * 0.25) + (min(total_reports, 40) / 40 * 10)
    score        += abuse_contrib

    # ── URLScan ─────────────────────────────────
    verdict = urlscan.get("verdict", "").lower()
    if verdict == "malicious":
        score += 15
    elif verdict == "suspicious":
        score += 8

    score = min(round(score), 100)

    # ── Thresholds ──────────────────────────────
    if score < 5:
        level = "Safe"
    elif score < 20:
        level = "Low Risk"
    elif score < 40:
        level = "Medium Risk"
    elif score < 60:
        level = "High Risk"
    else:
        level = "Critical"

    return score, level