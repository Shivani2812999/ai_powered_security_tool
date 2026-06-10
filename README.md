# 🛡️ AI Security Assessment Tool

An AI-powered cybersecurity system that analyzes **URLs, IP addresses, and files** to detect potential threats using external security APIs and generates **intelligent risk scores with AI-generated security reports**.

---

## 🚀 Features

- 🔍 Scan URLs, IP addresses, and files (PDF, EXE, ZIP)
- 🧠 Integrates multiple security APIs:
  - VirusTotal
  - AbuseIPDB
  - URLScan
- 📊 Custom Risk Scoring Engine (0–100 scale)
- ⚠️ Risk Levels:
  - Safe
  - Low Risk
  - Medium Risk
  - High Risk
  - Critical
 
 Examples:
  https://www.google.com/ ---------> safe
  1.1.1.1                 ----------> low risk
  https://bit.ly          ---------> medium risk
  http://www.eicar.org   ----------> high risk
  192.42.116.16       -----------> critical

    
- 🤖 AI-powered security report generation using LLMs
- 🖥️ Simple UI using Streamlit / Gradio
- ⚙️ Modular backend architecture

---

## 🏗️ System Architecture


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


---

## ⚙️ Tech Stack

- Python 🐍
- FastAPI / Flask (Backend APIs)
- Streamlit / Gradio (Frontend UI)
- REST APIs (VirusTotal, AbuseIPDB, URLScan)
- OpenAI / Gemini / Ollama (LLM Integration)
- Git & GitHub
- Docker (optional)

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-security-tool.git
cd ai-security-tool
2. Create virtual environment
python -m venv .venv

Activate:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file in root directory:

VIRUSTOTAL_API_KEY=your_key_here
ABUSEIPDB_API_KEY=your_key_here
URLSCAN_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
5. Run the application
If using FastAPI:
uvicorn backend.main:app --reload
If using Streamlit:
streamlit run frontend/app.py
🧠 How It Works
User submits input (URL, IP, or File)
System sends data to security APIs
API responses are normalized
Risk engine calculates unified risk score
LLM generates human-readable report
Results displayed in UI
📊 Risk Engine Logic

The system calculates risk based on weighted signals:

VirusTotal detections → malware/suspicious weighting
AbuseIPDB reputation → abuse confidence + report count
URLScan verdict → malicious/suspicious penalty

Final score is normalized between 0–100 and mapped to risk levels.

📌 Example Output
Risk Score: 67
Risk Level: High Risk
AI-Generated Report:
Multiple security engines flagged suspicious activity
Domain shows poor reputation history
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
🔮 Future Enhancements
🔥 Malware static & dynamic file analysis
🔥 RAG-based threat intelligence system
🔥 Vector database for historical threat tracking
🔥 Real-time monitoring dashboard
🔥 SaaS deployment for enterprise use
🎯 Use Cases
Cybersecurity analysts
SOC teams
Threat intelligence automation
Educational cybersecurity projects
Enterprise security monitoring tools
👨‍💻 Author

Shivani Hadapad
AI & Full Stack Developer
Python | Java | FastAPI | Machine Learning | Cybersecurity
