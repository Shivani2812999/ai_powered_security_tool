import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv


from services.virustotal import scan_url, scan_ip as vt_scan_ip, scan_file
from services.abuseipdb  import scan_ip  as abuse_scan_ip
from services.urlscan    import scan_url as urlscan_scan_url
from risk_engine         import calculate_risk
from ai_report           import generate_report

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(
    title="AnantNetra Security Assessment API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    target:    str
    scan_type: str


@app.get("/")
def home():
    return {
        "status":  "running",
        "service": "AnantNetra Security Assessment API"
    }


@app.post("/scan/url")
async def url_scan(req: ScanRequest):
    vt_result      = await scan_url(req.target)
    urlscan_result = await urlscan_scan_url(req.target)

    findings = {
        "virustotal": vt_result,
        "abuseipdb":  {},
        "urlscan":    urlscan_result,
    }

    score, level = calculate_risk(findings)
    ai_report    = generate_report(score, level, findings)

    return {
        "target":       req.target,
        "scan_type":    "url",
        "risk_score":   score,
        "risk_level":   level,
        "api_findings": findings,
        "ai_report":    ai_report
    }


@app.post("/scan/ip")
async def ip_scan(req: ScanRequest):
    vt_result    = await vt_scan_ip(req.target)
    abuse_result = await abuse_scan_ip(req.target)

    findings = {
        "virustotal": vt_result,
        "abuseipdb":  abuse_result,
        "urlscan":    {},
    }

    score, level = calculate_risk(findings)
    ai_report    = generate_report(score, level, findings)

    return {
        "target":       req.target,
        "scan_type":    "ip",
        "risk_score":   score,
        "risk_level":   level,
        "api_findings": findings,
        "ai_report":    ai_report
    }


@app.post("/scan/file")
async def file_scan(file: UploadFile = File(...)):
    file_bytes = await file.read()
    vt_result  = await scan_file(file.filename, file_bytes)

    findings = {
        "virustotal": vt_result,
        "abuseipdb":  {},
        "urlscan":    {},
        "filename":   file.filename,
        "size_bytes": len(file_bytes),
        "file_type":  file.content_type,
    }

    score, level = calculate_risk(findings)
    ai_report    = generate_report(score, level, findings)

    return {
        "target":       file.filename,
        "scan_type":    "file",
        "risk_score":   score,
        "risk_level":   level,
        "api_findings": findings,
        "ai_report":    ai_report
    }