import streamlit as st
import httpx
import json
import os
import re

st.set_page_config(
    page_title="AnantNetra – Security Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #F5F6FA; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }

.topbar {
    background: #ffffff;
    border-bottom: 1px solid #E5E7EB;
    padding: 0 2.5rem;
    height: 60px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.topbar-icon {
    width: 34px; height: 34px;
    background: #1D4ED8;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.topbar-name { font-size: 1rem; font-weight: 700; color: #111827; letter-spacing: -0.2px; }
.topbar-tagline {
    font-size: 0.75rem; color: #6B7280;
    border-left: 1px solid #E5E7EB; padding-left: 12px; margin-left: 4px;
}
.topbar-badge {
    margin-left: auto;
    background: #EFF6FF; color: #1D4ED8;
    font-size: 0.72rem; font-weight: 600;
    padding: 4px 10px; border-radius: 20px; border: 1px solid #BFDBFE;
}

.page-title { font-size: 1.35rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem; }
.page-subtitle { font-size: 0.85rem; color: #6B7280; margin-bottom: 1.75rem; }

.stRadio > label { display: none !important; }
div[role="radiogroup"] {
    display: flex; gap: 0;
    background: #F3F4F6; border-radius: 10px; padding: 4px;
    width: fit-content; margin-bottom: 1.5rem;
}
div[role="radiogroup"] label {
    background: transparent !important; border: none !important;
    border-radius: 7px !important; padding: 8px 20px !important;
    color: #6B7280 !important; font-size: 0.875rem !important;
    font-weight: 500 !important; cursor: pointer !important;
    transition: all 0.15s !important; white-space: nowrap !important;
}
div[role="radiogroup"] label:has(input:checked) {
    background: #ffffff !important; color: #111827 !important;
    font-weight: 600 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

.card {
    background: #ffffff; border: 1px solid #E5E7EB; border-radius: 14px;
    padding: 1.75rem; margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.card-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; color: #9CA3AF; margin-bottom: 0.6rem;
}
.card-body { font-size: 0.875rem; color: #374151; line-height: 1.7; }
.section-header {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; color: #6B7280;
    margin-bottom: 0.75rem; padding-bottom: 0.65rem; border-bottom: 1px solid #F3F4F6;
}

.rec-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #F9FAFB;
    font-size: 0.875rem;
    color: #374151;
    line-height: 1.6;
}
.rec-item:last-child { border-bottom: none; }
.rec-bullet {
    width: 6px; height: 6px; border-radius: 50%;
    background: #1D4ED8; flex-shrink: 0; margin-top: 7px;
}

.stTextInput > div > div > input {
    background: #F9FAFB !important; border: 1px solid #E5E7EB !important;
    border-radius: 10px !important; color: #111827 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important;
    padding: 11px 14px !important; transition: all 0.15s !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
}
.stTextInput > div > div > input:focus {
    background: #ffffff !important; border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}
.stTextInput > label { font-size: 0.8rem !important; font-weight: 600 !important; color: #374151 !important; }

.stButton > button {
    background: #1D4ED8 !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    padding: 11px 24px !important; letter-spacing: 0.1px !important;
    box-shadow: 0 1px 3px rgba(29,78,216,0.3), 0 4px 12px rgba(29,78,216,0.15) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #1E40AF !important; transform: translateY(-1px) !important;
    box-shadow: 0 2px 6px rgba(29,78,216,0.35), 0 6px 16px rgba(29,78,216,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stFileUploader > div {
    background: #F9FAFB !important; border: 2px dashed #D1D5DB !important;
    border-radius: 12px !important; transition: border-color 0.2s !important;
}
.stFileUploader > div:hover { border-color: #3B82F6 !important; }

.metrics-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem; }
.metric-box {
    background: #ffffff; border: 1px solid #E5E7EB; border-radius: 14px;
    padding: 1.4rem 1.6rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-box-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; color: #9CA3AF; margin-bottom: 8px;
}
.metric-box-value { font-size: 2.4rem; font-weight: 700; line-height: 1; color: #111827; }
.metric-box-value.danger { color: #DC2626; }
.metric-box-value.warning { color: #D97706; }
.metric-box-value.safe { color: #059669; }
.metric-box-sub { font-size: 0.75rem; color: #9CA3AF; margin-top: 6px; }

.empty-state { text-align: center; padding: 5rem 2rem; }
.empty-state-icon { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.35; }
.empty-state-title { font-size: 1rem; font-weight: 600; color: #6B7280; margin-bottom: 6px; }
.empty-state-sub { font-size: 0.85rem; color: #9CA3AF; }

.error-card {
    background: #FEF2F2; border: 1px solid #FECACA; border-radius: 12px;
    padding: 1.1rem 1.4rem; color: #991B1B; font-size: 0.875rem;
    font-weight: 500; margin-bottom: 1.25rem;
}
.error-card .err-detail { color: #B91C1C; font-weight: 400; margin-top: 4px; font-size: 0.82rem; }

.stDownloadButton > button {
    background: #ffffff !important; color: #1D4ED8 !important;
    border: 1px solid #BFDBFE !important; border-radius: 10px !important;
    font-weight: 600 !important; box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: #EFF6FF !important; transform: none !important; box-shadow: none !important;
}

.stSpinner > div { border-top-color: #1D4ED8 !important; }
hr { border-color: #F3F4F6 !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for key, val in [("page", "scan"), ("result", None), ("error_msg", None)]:
    if key not in st.session_state:
        st.session_state[key] = val


def call_api(endpoint, payload=None, files=None):
    try:
        with httpx.Client(timeout=60) as client:
            if files:
                resp = client.post(f"{API_BASE}{endpoint}", files=files)
            else:
                resp = client.post(f"{API_BASE}{endpoint}", json=payload)
            resp.raise_for_status()
            return resp.json(), None
    except httpx.ConnectError:
        return None, "Cannot connect to backend. Make sure the FastAPI server is running."
    except httpx.HTTPStatusError as e:
        return None, f"Server returned {e.response.status_code}."
    except Exception as e:
        return None, str(e)


def render_recommendations(content: str) -> str:
    """Split numbered recommendations into bullet items."""
    lines = re.split(r'\d+\.', content)
    lines = [l.strip() for l in lines if l.strip()]
    if not lines:
        return f'<div class="card-body">{content}</div>'
    items = "".join(
        f'<div class="rec-item"><div class="rec-bullet"></div><div>{line}</div></div>'
        for line in lines
    )
    return items


# ── Top bar ──
st.markdown("""
<div class="topbar">
    <div class="topbar-icon">🛡️</div>
    <span class="topbar-name">AnantNetra</span>
    <span class="topbar-tagline">Security Assessment Platform</span>
    <div class="topbar-badge">Shivani Hadapad (Developer)</div>
</div>
""", unsafe_allow_html=True)

# ── Centered layout ──
_, main, _ = st.columns([1, 5, 1])

with main:
    st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)

    # Tab nav
    c1, c2, c_rest = st.columns([1.3, 1.3, 5])
    with c1:
        if st.button("🔍  Scan", use_container_width=True):
            st.session_state.page = "scan"
            st.rerun()
    with c2:
        if st.button("📊  Results", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # ════════════════════════
    # SCAN PAGE
    # ════════════════════════
    if st.session_state.page == "scan":
        st.markdown('<div class="page-title">New Scan</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Choose a target type, enter a value, and run the analysis.</div>', unsafe_allow_html=True)

        scan_type = st.radio("type", ["URL", "IP Address", "File"], horizontal=True)

        if scan_type == "URL":
            st.markdown('<div class="card"><div class="card-label">Target URL</div>', unsafe_allow_html=True)
            url = st.text_input("URL", placeholder="https://example.com", label_visibility="collapsed")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if st.button("Run URL Scan →", use_container_width=True):
                if not url.strip():
                    st.warning("Enter a URL to continue.")
                else:
                    with st.spinner("Running threat analysis…"):
                        result, error = call_api("/scan/url", {"target": url, "scan_type": "url"})
                        st.session_state.result = result
                        st.session_state.error_msg = error
                        st.session_state.page = "results"
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif scan_type == "IP Address":
            st.markdown('<div class="card"><div class="card-label">IP Address</div>', unsafe_allow_html=True)
            ip = st.text_input("IP", placeholder="8.8.8.8", label_visibility="collapsed")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if st.button("Run IP Scan →", use_container_width=True):
                if not ip.strip():
                    st.warning("Enter an IP address to continue.")
                else:
                    with st.spinner("Querying threat intelligence APIs…"):
                        result, error = call_api("/scan/ip", {"target": ip, "scan_type": "ip"})
                        st.session_state.result = result
                        st.session_state.error_msg = error
                        st.session_state.page = "results"
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif scan_type == "File":
            st.markdown('<div class="card"><div class="card-label">Upload File</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Drop file here", type=["exe", "zip", "pdf"], label_visibility="collapsed")
            st.markdown('<div style="font-size:0.75rem;color:#9CA3AF;margin-top:2px;">Supported: .exe · .zip · .pdf</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
            if st.button("Analyze File →", use_container_width=True):
                if uploaded_file is None:
                    st.warning("Upload a file to continue.")
                else:
                    with st.spinner("Uploading and scanning…"):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        result, error = call_api("/scan/file", files=files)
                        st.session_state.result = result
                        st.session_state.error_msg = error
                        st.session_state.page = "results"
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex;gap:0;background:#ffffff;border:1px solid #E5E7EB;
                    border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.04);overflow:hidden;
                    margin-top:0.5rem;">
            <div style="flex:1;padding:1.1rem 1.3rem;border-right:1px solid #F3F4F6;">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Intelligence Sources</div>
                <div style="font-size:0.82rem;color:#374151;">VirusTotal · AbuseIPDB · URLScan.io</div>
            </div>
            <div style="flex:1;padding:1.1rem 1.3rem;border-right:1px solid #F3F4F6;">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Analysis</div>
                <div style="font-size:0.82rem;color:#374151;">LLM-generated threat summary</div>
            </div>
            <div style="flex:1;padding:1.1rem 1.3rem;">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Output</div>
                <div style="font-size:0.82rem;color:#374151;">Risk score + remediation steps</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════
    # RESULTS PAGE
    # ════════════════════════
    elif st.session_state.page == "results":
        st.markdown('<div class="page-title">Assessment Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">AI-generated threat intelligence report.</div>', unsafe_allow_html=True)

        if st.session_state.error_msg:
            st.markdown(f"""
            <div class="error-card">
                ⚠ Connection error
                <div class="err-detail">{st.session_state.error_msg}</div>
            </div>""", unsafe_allow_html=True)

        elif st.session_state.result:
            result = st.session_state.result
            risk_score = result.get("risk_score", "—")
            risk_level = result.get("risk_level", "Unknown")

            try:
                score_int = int(risk_score)
                score_cls = "danger" if score_int >= 70 else "warning" if score_int >= 40 else "safe"
            except Exception:
                score_cls = ""
            level_cls = ("danger" if risk_level.lower() in ("high risk", "critical")
                         else "warning" if "medium" in risk_level.lower() else "safe")

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-box-label">Risk Score</div>
                    <div class="metric-box-value {score_cls}">{risk_score}
                        <span style="font-size:1rem;color:#9CA3AF;font-weight:400"> /100</span>
                    </div>
                    <div class="metric-box-sub">Aggregate threat score</div>
                </div>
                <div class="metric-box">
                    <div class="metric-box-label">Threat Level</div>
                    <div class="metric-box-value {level_cls}">{risk_level}</div>
                    <div class="metric-box-sub">Classification</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            ai_report = result.get("ai_report", {})

            for section_key, section_title in [
                ("executive_summary", "Executive Summary"),
                ("recommendations", "Recommendations"),
                ("technical_details", "Technical Details"),
            ]:
                content = ai_report.get(section_key, "")
                if content:
                    if section_key == "recommendations":
                        body_html = render_recommendations(content)
                    else:
                        body_html = f'<div class="card-body">{content}</div>'

                    st.markdown(f"""
                    <div class="card">
                        <div class="section-header">{section_title}</div>
                        {body_html}
                    </div>""", unsafe_allow_html=True)

            findings = result.get("api_findings", {})
            if findings:
                with st.expander("Raw API Findings"):
                    st.json(findings)

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.download_button(
                label="⬇  Download Report (JSON)",
                data=json.dumps(result, indent=2),
                file_name="anantnetra_report.json",
                mime="application/json",
                use_container_width=True
            )

        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-title">No results yet</div>
                <div class="empty-state-sub">Run a scan from the Scan tab to see your report here.</div>
            </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="border-top:1px solid #E5E7EB;padding-top:1.25rem;display:flex;
                justify-content:space-between;align-items:center;
                font-size:0.75rem;color:#9CA3AF;">
        <span>Developer: Shivani Hadapad</span>
        <span>AI-Powered Security Assessment</span>
    </div>
    """, unsafe_allow_html=True)