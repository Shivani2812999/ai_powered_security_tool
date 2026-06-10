import os
import asyncio
import httpx

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("URLSCAN_API_KEY")


async def scan_url(url: str) -> dict:

    # graceful fallback if key not configured
    if not API_KEY:
        return {"verdict": "", "score": 0, "categories": []}

    headers = {
        "API-Key":      API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "url":        url,
        "visibility": "public"
    }

    async with httpx.AsyncClient(timeout=60) as client:

        submit = await client.post(
            "https://urlscan.io/api/v1/scan/",
            headers=headers,
            json=payload
        )
        if submit.status_code != 200:
            return {"verdict": "", "score": 0, "categories": []}

        scan_uuid = submit.json().get("uuid")
        if not scan_uuid:
            return {"verdict": "", "score": 0, "categories": []}

        for _ in range(12):
            await asyncio.sleep(5)

            result = await client.get(
                f"https://urlscan.io/api/v1/result/{scan_uuid}/",
                headers=headers
            )
            if result.status_code == 200:
                data = result.json()
                verdict = (
                    data.get("verdicts", {})
                        .get("overall", {})
                        .get("verdict", "")
                )
                score = (
                    data.get("verdicts", {})
                        .get("overall", {})
                        .get("score", 0)
                )
                categories = (
                    data.get("verdicts", {})
                        .get("overall", {})
                        .get("categories", [])
                )
                return {
                    "verdict":    verdict,
                    "score":      score,
                    "categories": categories,
                }

    return {"verdict": "", "score": 0, "categories": []}