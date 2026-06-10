import os
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")


async def scan_ip(ip: str) -> dict:
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers=headers,
            params=params
        )
        if response.status_code != 200:
            return {"error": response.text}

        data = response.json()["data"]
        return {
            "abuseConfidenceScore": data.get("abuseConfidenceScore", 0),
            "totalReports":         data.get("totalReports",         0),
            "country":              data.get("countryCode",          ""),
            "isp":                  data.get("isp",                  ""),
        }