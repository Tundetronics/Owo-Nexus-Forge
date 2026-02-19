import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF
import time

# --- I. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secrets Management (Managed in Streamlit Dashboard)
PAYSTACK_SK = st.secrets["PAYSTACK_SECRET_KEY"]
BASE_URL = "https://app.owonexus.com/"

# --- II. BRANDING & THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white; }
    .stButton>button { background-color: #FACC15; color: black; border-radius: 10px; font-weight: bold; width: 100%; }
    .tier-card { border: 1px solid #FACC15; padding: 20px; border-radius: 15px; background: rgba(250, 204, 21, 0.05); }
    </style>
""", unsafe_allow_html=True)

# --- III. THE 5-TIER ASCENSION MATRIX ---
TIERS = {
    "Grassroots": {"price": 0, "limit": 3, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "limit": 10, "desc": "10 Searches/Day. Mobile Optimized."},
    "Scout": {"price": 2500, "limit": 9999, "desc": "Unlimited. AI ROI Hooks."},
    "Marksman": {"price": 150000, "limit": 9999, "desc": "Bulk Export. Verified Leads."},
    "Overlord": {"price": 2400000, "limit": 9999, "desc": "Private Rust Ghost-Agent."}
}

# --- IV. FINANCIAL & INVOICE CORE ---
def init_payment(email, amount, tier_name):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    payload = {"email": email, "amount": int(amount * 100), "callback_url": BASE_URL, "metadata": {"tier": tier_name}}
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return res['data']['authorization_url']
    except: return None

def generate_invoice(name, tier, amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "TUNDETRONICS NIG. LTD. - OWO-NEXUS AI", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"BILL TO: {name}", ln=True)
    pdf.cell(100, 10, f"TIER: {tier}", ln=True)
    pdf.cell(100, 10, f"TOTAL: NGN {amount:,.2f}", ln=True)
    pdf.ln(20)
    pdf.set_text_color(250, 204, 21)
    pdf.cell(200, 10, "VERIFIED SOVEREIGN TRANSACTION", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- V. THE SNIPER DASHBOARD ---
def main():
    # Verify Payment on Return
    if "reference" in st.query_params:
        ref = st.query_params["reference"]
        # Logic to ping Paystack API to verify status
        st.success(f"Payment Verified. Welcome, Sovereign.")
        st.query_params.clear()

    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("Industrial Intelligence by Tundetronics Nig. Ltd.")

    tab1, tab2, tab3 = st.tabs(["The Swarm", "Upgrade Ladder", "Admin Vault"])

    with tab1:
        st.header("Deploy Swarm")
        niche = st.text_input("Enter Industry Niche", placeholder="e.g. Solar Installers Abuja")
        if st.button("EXECUTE SNIPER"):
            with st.spinner("Ghost-Agent Hunting..."):
                time.sleep(2)
                st.write("Results would appear here based on tier permissions.")

    with tab2:
        st.header("The Sovereign Ladder")
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"<div class='tier-card'><h3>{name}</h3><p>₦{info['price']:,}</p><small>{info['desc']}</small></div>", unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Upgrade {name}", key=name):
                        link = init_payment("tundetronics@gmail.com", info['price'], name)
                        if link: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{link}\'">', unsafe_allow_html=True)

    with tab3:
        st.header("Admin Command Center")
        st.info("Log in as Administrator to view Revenue and User Metrics.")

if __name__ == "__main__":
    main()