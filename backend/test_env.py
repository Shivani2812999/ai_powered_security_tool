from dotenv import load_dotenv
import os
load_dotenv()

print("VT KEY:", os.getenv("VIRUSTOTAL_API_KEY", "NOT FOUND"))
print("ABUSE KEY:", os.getenv("ABUSEIPDB_API_KEY", "NOT FOUND"))
print("URLSCAN KEY:", os.getenv("URLSCAN_API_KEY", "NOT FOUND"))