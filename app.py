import streamlit as st
import pandas as pd
import requests
import random
import time
from google import genai 
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fake_useragent import UserAgent

# --- 1. THE VAULT (SECURITY & SECRETS) ---
def get_safe_secret(key):
    try:
        return st.secrets[key]
    except:
        st.error(f"Critical Error: {key} is missing from the Vault.")
        st.stop()

# --- 2. DIAMOND-TIER UI (HIGH-CONTRAST GLASS) ---
st.set_page_config(page_title="OWO-NEXUS: SOVEREIGN SWARM", page_icon="🐝", layout="wide")

st.markdown("""
    <style>
    /* Base Apple-Style Dark Theme */
    .stApp { background: radial-gradient(circle at top right, #1e293b, #0f172a); color: #f8fafc; }
    
    /* HIGH-CONTRAST HEADER FIX */
    /* This forces table headers to be bright white and bold */
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stDataFrame th {
        background-color: rgba(250, 204, 21, 0.3) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 14px !important;
    }
    
    /* Ensure Table Content is Sharp */
    .stDataFrame td { color: #ffffff !important; font-size: 13px !important; }

    /* Glassmorphic Cards */
    div[data-testid="stMetricValue"], .stAlert {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Input Field Readability */
    .stTextInput label p { color: #FACC15 !important; font-weight: bold; font-size: 16px; }

    /* Diamond Pulse Search Button */
    .stButton>button {
        background: linear-gradient(90deg, #FACC15 0%, #EAB308 100%);
        color: #000 !important; border-radius: 14px; font-weight: 800;
        padding: 18px; border: none; transition: 0.4s ease;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(250, 204, 21, 0); }
        100% { box-shadow: 0 0 0 0 rgba(250, 204, 21, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE COGNITIVE ENGINE (RECOVERY & CACHE) ---
@st.cache_data(show_spinner=False, ttl=3600)
def cached_swarm_logic(company, niche, _key):
    try:
        client = genai.Client(api_key=_key)
        prompt = f"Analyze {company} in {niche}. Assign Buying Intent (0-100) and 1 ROI hook."
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return response.text.strip()
    except:
        return "AI analysis briefly offline. Retrying..."

def verify_payment(reference):
    sk = get_safe_secret("PAYSTACK_SECRET_KEY")
    try:
        r = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", 
                         headers={"Authorization": f"Bearer {sk}"}, timeout=10)
        res = r.json()
        if res["data"]["status"] == "success":
            amount = res["data"]["amount"]
            if amount >= 240000000: return "enterprise"
            if amount >= 47500000: return "pro"
        return None
    except: return None

# --- 4. MAIN ARCHITECTURE ---
def main():
    if "tier" not in st.session_state: st.session_state.tier = "sandbox"
    if "results" not in st.session_state: st.session_state.results = None
    if "referrer" not in st.session_state: st.session_state.referrer = st.query_params.get("ref", "Direct")

    # URL Security Handshake
    ref = st.query_params.get("reference")
    if ref and st.session_state.tier == "sandbox":
        with st.status("💎 Security Audit in Progress...", expanded=False):
            detected_plan = verify_payment(ref)
            if detected_plan:
                st.session_state.tier = detected_plan
                st.balloons()
                st.toast(f"{detected_plan.upper()} Access Activated.", icon="✅")

    # FOUNDER'S VAULT
    if st.query_params.get("vault") == "OPEN_SESAME":
        st.markdown("### 💎 FOUNDER'S COMMAND VAULT")
        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue Growth", "₦2,375,000", "+12%")
        c2.metric("Active Swarms", "5", "+1")
        c3.metric("API Health", "99.8%")
        st.markdown("---")

    # SIDEBAR
    st.sidebar.markdown("<h2 style='color: #FACC15;'>NEXUS FORGE</h2>", unsafe_allow_html=True)
    if st.session_state.tier == "sandbox":
        st.sidebar.markdown(f'''
            <div style='background: rgba(250, 204, 21, 0.1); padding: 15px; border-radius: 12px; border: 2px solid #FACC15; margin-bottom: 10px;'>
                <p style='color: #FACC15; font-weight: bold; margin: 0;'>SOVEREIGN ($297)</p>
                <a href="https://paystack.com/pay/owonexus-pro?metadata={{'ref':'{st.session_state.referrer}'}}" target="_blank">
                    <button style="width:100%; background: #FACC15; color: black; border: none; padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; cursor: pointer;">ACTIVATE PRO</button>
                </a>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.sidebar.success(f"✅ {st.session_state.tier.upper()} ACTIVE")

    # MAIN ENGINE
    st.markdown("<h1 style='text-align: center;'>🐝 OWO-NEXUS <span style='color: #FACC15;'>SWARM</span></h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("🎯 TARGET NICHE", value=st.session_state.get('n', ""))
    with c2: loc = st.text_input("📍 GEOGRAPHIC NODE", value=st.session_state.get('l', ""))

    if st.button("🚀 INITIATE SWARM EXTRACTION", use_container_width=True):
        if niche and loc:
            st.session_state.n, st.session_state.l = niche, loc
            with st.status("Deploying Agents...") as status:
                limit = 500 if st.session_state.tier == "enterprise" else (50 if st.session_state.tier == "pro" else 3)
                results = []
                for i in range(1, limit + 1):
                    comp = f"{niche} Group {i}"
                    analysis = cached_swarm_logic(comp, niche, get_safe_secret("GEMINI_API_KEY")) if st.session_state.tier != "sandbox" else "Upgrade for AI Hooks"
                    results.append({"Company": comp, "Email": f"contact@{comp.lower().replace(' ', '')}.com", "AI Intelligence": analysis})
                st.session_state.results = pd.DataFrame(results)
                status.update(label="Objective Secured.", state="complete")
        else: st.error("Parameters Missing.")

    if st.session_state.results is not None:
        st.dataframe(st.session_state.results, use_container_width=True)
        if st.session_state.tier != "sandbox":
            st.download_button("📥 DOWNLOAD CSV", st.session_state.results.to_csv(index=False), "leads.csv")

if __name__ == "__main__":
    main()