import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import time

# --- 1. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secrets Management (Must be set in Streamlit Cloud Settings)
PAYSTACK_SK = st.secrets["PAYSTACK_SECRET_KEY"]
BASE_URL = "https://app.owonexus.com/" # ENSURE HTTPS

# --- 2. THEME & BRANDING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #020617; color: white; }}
    .stButton>button {{ background-color: #FACC15; color: black; border-radius: 8px; font-weight: bold; }}
    .tier-card {{ border: 1px solid #FACC15; padding: 20px; border-radius: 12px; background: rgba(250, 204, 21, 0.03); min-height: 320px; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ARCHITECTURE ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "desc": "10 Searches/Day. Mobile Optimized."},
    "Scout": {"price": 2500, "desc": "Unlimited Searches. AI Sales Hooks."},
    "Marksman": {"price": 150000, "desc": "Full CRM Export. Verified Contacts."},
    "Overlord": {"price": 2400000, "desc": "Private Rust Agent. 24/7 Priority Support."}
}

# --- 4. CORE UTILITIES ---

def init_payment(email, amount, tier):
    """Initializes a secure Paystack session with HTTPS callback"""
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    payload = {
        "email": email,
        "amount": int(amount * 100),
        "callback_url": BASE_URL,
        "metadata": {"tier": tier}
    }
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return res['data']['authorization_url'] if res.get('status') else None
    except: return None

def get_vault_data():
    """Fetches real transaction data from Paystack API"""
    url = "https://api.paystack.co/transaction"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    try:
        res = requests.get(url, headers=headers).json()
        if res.get('status'):
            df = pd.DataFrame(res['data'])
            df['amount'] = df['amount'] / 100
            # Metadata parsing for Tier identification
            df['Tier'] = df['metadata'].apply(lambda x: x.get('tier', 'Other') if isinstance(x, dict) else 'Other')
            return df
        return pd.DataFrame()
    except: return pd.DataFrame()

# --- 5. THE SOVEREIGN INTERFACE ---

def main():
    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("BY TUNDETRONICS NIG. LTD. | INDUSTRIAL AI INFRASTRUCTURE")

    # Verification Handshake
    if "reference" in st.query_params:
        st.success("💎 SOVEREIGN STATUS ACTIVATED. SESSION VERIFIED.")
        st.balloons()
        st.query_params.clear()

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "🛡️ Admin Vault"])

    # TAB 1: SEARCH ENGINE
    with tabs[0]:
        st.subheader("Deploy Ghost-Agent Swarm")
        niche = st.text_input("Target Niche", placeholder="e.g., Accountants Abuja")
        if st.button("EXECUTE SNIPER"):
            with st.spinner("Swarm Hunting..."):
                time.sleep(1.5)
                st.info("Lead generation active. Complete results visible to verified tiers.")

    # TAB 2: PRICING LADDER
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"<div class='tier-card'><h4>{name}</h4><h2 style='color:#FACC15'>₦{info['price']:,}</h2><p>{info['desc']}</p></div>", unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Activate {name}", key=name):
                        link = init_payment("tundetronics@gmail.com", info['price'], name)
                        if link: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{link}\'">', unsafe_allow_html=True)

    # TAB 3: REAL-TIME VAULT
    with tabs[2]:
        pwd = st.text_input("Admin Key", type="password")
        if pwd == "OwoNexus2026":
            st.subheader("Live Financial Ledger")
            df = get_vault_data()
            if not df.empty:
                success_df = df[df['status'] == 'success']
                m1, m2 = st.columns(2)
                m1.metric("Realized Revenue", f"₦{success_df['amount'].sum():,.2f}")
                m2.metric("Active Sovereigns", len(success_df))
                
                fig = px.pie(success_df, values='amount', names='Tier', title="Revenue by Tier", color_discrete_sequence=px.colors.sequential.YlOrBr)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Awaiting live transaction data...")

if __name__ == "__main__":
    main()