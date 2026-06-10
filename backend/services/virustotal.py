import os
import base64
import asyncio
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY  = os.getenv("VIRUSTOTAL_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3"
HEADERS  = {"x-apikey": API_KEY}


def _parse_stats(data: dict) -> dict:
    stats = (
        data.get("data", {})
            .get("attributes", {})
            .get("last_analysis_stats", {})
    )
    return {
        "malicious":  stats.get("malicious",  0),
        "suspicious": stats.get("suspicious", 0),
        "harmless":   stats.get("harmless",   0),
        "undetected": stats.get("undetected", 0),
    }


async def scan_url(url: str) -> dict:
    url_id = base64.urlsafe_b64encode(
        url.encode()
    ).decode().strip("=")

    async with httpx.AsyncClient(timeout=30) as client:
        await client.post(
            f"{BASE_URL}/urls",
            headers=HEADERS,
            data={"url": url}
        )
        response = await client.get(
            f"{BASE_URL}/urls/{url_id}",
            headers=HEADERS
        )
        if response.status_code != 200:
            return {"error": response.text}
        return _parse_stats(response.json())


# async def scan_ip(ip: str) -> dict:
#     async with httpx.AsyncClient(timeout=30) as client:
#         response = await client.get(
#             f"{BASE_URL}/ip_addresses/{ip}",
#             headers=HEADERS
#         )
#         if response.status_code != 200:
#             return {"error": response.text}
#         return _parse_stats(response.json())

async def scan_ip(ip: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{BASE_URL}/ip_addresses/{ip}",
            headers=HEADERS
        )
        if response.status_code != 200:
            return {"malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}

        data  = response.json()
        attrs = data.get("data", {}).get("attributes", {})

        # IP endpoint stores stats here, not last_analysis_stats
        stats = attrs.get("last_analysis_stats", {})

        print(f"[VT IP DEBUG] raw attrs keys: {list(attrs.keys())}")
        print(f"[VT IP DEBUG] stats: {stats}")

        return {
            "malicious":  stats.get("malicious",  0),
            "suspicious": stats.get("suspicious", 0),
            "harmless":   stats.get("harmless",   0),
            "undetected": stats.get("undetected", 0),
        }


async def scan_file(filename: str, file_bytes: bytes) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:

        upload_response = await client.post(
            f"{BASE_URL}/files",
            headers=HEADERS,
            files={"file": (filename, file_bytes)}
        )
        if upload_response.status_code != 200:
            return {"error": upload_response.text}

        analysis_id = (
            upload_response.json()
                           .get("data", {})
                           .get("id")
        )
        if not analysis_id:
            return {"error": "No analysis ID returned from VirusTotal"}

        for _ in range(10):
            await asyncio.sleep(3)

            result_response = await client.get(
                f"{BASE_URL}/analyses/{analysis_id}",
                headers=HEADERS
            )
            if result_response.status_code != 200:
                return {"error": result_response.text}

            result_data = result_response.json()
            status = (
                result_data.get("data", {})
                           .get("attributes", {})
                           .get("status")
            )
            if status == "completed":
                stats = (
                    result_data.get("data", {})
                               .get("attributes", {})
                               .get("stats", {})
                )
                return {
                    "malicious":  stats.get("malicious",  0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless":   stats.get("harmless",   0),
                    "undetected": stats.get("undetected", 0),
                }

        return {"error": "Analysis timed out after 30 seconds"}