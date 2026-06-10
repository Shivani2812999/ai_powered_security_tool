🛡️ AI Security Assessment Tool

An AI-powered cybersecurity system that analyzes URLs, IP addresses, and files to detect potential threats using security APIs and generates intelligent risk scores with AI-generated reports.

🚀 Features
🔍 Scan URLs, IP addresses, and files
🧠 Integrates multiple security APIs:
VirusTotal
AbuseIPDB
URLScan
📊 Custom Risk Scoring Engine (0–100)
⚠️ Risk Classification:
Safe
Low Risk
Medium Risk
High Risk
Critical
🤖 AI-generated security report (LLM-based)
🖥️ Simple UI using Streamlit / Gradio
📄 Clean API-based architecture
🏗️ System Architecture
User Input (URL / IP / File)
        ↓
Security API Layer
(VirusTotal / AbuseIPDB / URLScan)
        ↓
Data Processing Layer
        ↓
Risk Scoring Engine
        ↓
AI Report Generator (LLM)
        ↓
Frontend UI (Streamlit / Gradio)
⚙️ Tech Stack
Python 🐍
FastAPI / Flask (Backend APIs)
Streamlit / Gradio (Frontend UI)
REST APIs (VirusTotal, AbuseIPDB, URLScan)
OpenAI / Gemini / Ollama (LLM)
Git & GitHub
Docker (optional)
📦 Installation
1. Clone Repository
git clone https://github.com/your-username/ai-security-tool.git
cd ai-security-tool
2. Create Virtual Environment
python -m venv .venv

Activate:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Add Environment Variables

Create a .env file:

VIRUSTOTAL_API_KEY=your_key
ABUSEIPDB_API_KEY=your_key
URLSCAN_API_KEY=your_key
OPENAI_API_KEY=your_key
5. Run the Application

If FastAPI:

uvicorn backend.main:app --reload

If Streamlit:

streamlit run frontend/app.py
🧠 How It Works
User submits input (URL/IP/File)
System calls security APIs
Data is normalized and processed
Risk engine calculates score
AI model generates human-readable report
Results displayed in UI
📊 Risk Engine Logic
VirusTotal detections → weighted scoring
AbuseIPDB reputation → abuse confidence impact
URLScan verdict → malicious/suspicious penalty
Final score normalized to 0–100 scale
📌 Example Output
Risk Score: 67
Risk Level: High Risk
AI Report:
Suspicious activity detected
Multiple security vendor flags
Recommendation: Avoid interacting with this resource

📁 Project Structure
ai-security-tool/
│
├── backend/
│   ├── main.py
│   ├── risk_engine.py
│   ├── api_clients.py
│
├── frontend/
│   ├── app.py
│
├── .venv/
├── requirements.txt
├── .env
├── README.md

👨‍💻 Author

Shivani Hadapad
AI & Full Stack Developer
Python | Java | FastAPI | Machine Learning | Cybersecurity
