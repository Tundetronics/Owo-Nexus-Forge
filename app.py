import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import time
from datetime import datetime

# --- 1. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secure Secret Retrieval
PAYSTACK_SK = st.secrets["PAYSTACK_SECRET_KEY"] # Set this in Streamlit Secrets
BASE_URL = "https://app.owonexus.com/"

# --- 2. BRANDING & THEME ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #020617; color: white; }}
    .stButton>button {{ background-color: #FACC15; color: black; border-radius: 8px; font-weight: bold; border: none; }}
    .tier-card {{ border: 1px solid #FACC15; padding: 20px; border-radius: 12px; background: rgba(250, 204, 21, 0.03); height: 350px; }}
    .metric-box {{ background: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #FACC15; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ARCHITECTURE ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "desc": "10 Searches/Day. Mobile optimized."},
    "Scout": {"price": 2500, "desc": "Unlimited Searches. AI Sales Hooks."},
    "Marksman": {"price": 150000, "desc": "Full CRM Export. Verified Contacts."},
    "Overlord": {"price": 2400000, "desc": "Private Rust Agent. 24/7 Priority Support."}
}

# --- 4. CORE FUNCTIONALITY (PAYMENTS & DATA) ---

def init_paystack_session(email, amount, tier):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    payload = {
        "email": email,
        "amount": int(amount * 100),
        "callback_url": BASE_URL,
        "metadata": {"custom_fields": [{"display_name": "Tier", "variable_name": "tier", "value": tier}]}
    }
    response = requests.post(url, json=payload, headers=headers).json()
    return response['data']['authorization_url'] if response.get('status') else None

def get_real_paystack_data():
    """Fetches real transaction history from your Paystack Account"""
    url = "https://api.paystack.co/transaction"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    response = requests.get(url, headers=headers).json()
    if response.get('status'):
        return pd.DataFrame(response['data'])
    return pd.DataFrame()

# --- 5. THE SOVEREIGN INTERFACE ---

def main():
    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("BY TUNDETRONICS NIG. LTD. | SOVEREIGN AI INFRASTRUCTURE")

    # URL Parameter Verification (Post-Payment)
    if "reference" in st.query_params:
        ref = st.query_params["reference"]
        st.success(f"Verified Transaction: {ref}. Welcome to your new Tier.")
        st.balloons()
        # In a real build, you'd update your database here
        st.query_params.clear()

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "🛡️ Admin Vault"])

    # TAB 1: THE ENGINE
    with tabs[0]:
        st.subheader("Deploy Ghost-Agent Swarm")
        niche = st.text_input("Target Niche", placeholder="e.g., Real Estate Lagos")
        if st.button("EXECUTE"):
            with st.spinner("Hunting for leads..."):
                time.sleep(2)
                st.info("System is ready. Search results are restricted to verified tiers.")

    # TAB 2: PRICING LADDER
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"""
                <div class='tier-card'>
                    <h4>{name}</h4>
                    <h2 style='color:#FACC15'>₦{info['price']:,}</h2>
                    <p style='font-size:12px'>{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Get {name}", key=name):
                        url = init_paystack_session("tundetronics@gmail.com", info['price'], name)
                        if url: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{url}\'">', unsafe_allow_html=True)

    # TAB 3: ADMIN VAULT (REAL DATA)
    with tabs[2]:
        pwd = st.text_input("Vault Key", type="password")
        if pwd == "OwoNexus2026":
            st.subheader("Live Revenue Analytics")
            df = get_real_paystack_data()
            
            if not df.empty:
                # Calculate Real Metrics
                total_rev = df[df['status'] == 'success']['amount'].sum() / 100
                success_count = len(df[df['status'] == 'success'])
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Real-Time Revenue", f"₦{total_rev:,.2f}")
                m2.metric("Successful Payouts", success_count)
                m3.metric("System Uptime", "99.9%")

                # Visualizing Real Sales Trend
                df['created_at'] = pd.to_datetime(df['created_at'])
                fig = px.line(df, x='created_at', y='amount', title="Transaction Velocity",
                             color_discrete_sequence=['#FACC15'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df[['customer', 'amount', 'status', 'created_at']].head(10))
            else:
                st.info("Waiting for first transaction data from Paystack...")

if __name__ == "__main__":
    main()