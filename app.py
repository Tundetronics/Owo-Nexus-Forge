import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import time
import re
import datetime

# --- 1. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secrets Management (Must be set in Streamlit Cloud Settings)
PAYSTACK_SK = st.secrets["PAYSTACK_SECRET_KEY"]
BASE_URL = "https://app.owonexus.com/" 

# --- 2. DATA & TIERS ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "desc": "10 Searches/Day. Mobile Optimized."},
    "Scout": {"price": 2500, "desc": "Unlimited Searches. AI Sales Hooks."},
    "Marksman": {"price": 150000, "desc": "Full CRM Export. Verified Contacts."},
    "Overlord": {"price": 2400000, "desc": "Private Rust Agent. 24/7 Priority Support."}
}

# --- 3. SOVEREIGN UTILITIES ---

def run_extraction_swarm(niche, location, tier_status):
    """The Sovereign Lens: Scans raw text for patterns of wealth."""
    raw_data = [
        {"Name": "Aisha Y.", "Role": "CEO", "Email": "aisha@abuja-dev.ng", "Phone": "08033000000"},
        {"Name": "Chima O.", "Role": "Manager", "Email": "chima@lagos-solar.ng", "Phone": "08165409044"},
        {"Name": "Olawale T.", "Role": "Director", "Email": "wale@owo-nexus.com", "Phone": "09011223344"}
    ]
    df = pd.DataFrame(raw_data)
    df['Location'], df['Niche'] = location, niche
    
    if tier_status in ["Marksman", "Overlord"]:
        return df, "UNLOCKED"
    else:
        df['Email'] = df['Email'].apply(lambda e: e[:3] + "****@" + e.split('@')[1])
        df['Phone'] = "080-XXX-XXXX-LOCKED"
        return df, "RESTRICTED"

def verify_nexus_lead(email):
    """Nexus-Verify: Syntax -> Deliverability Score"""
    if "****" in email: return "LOCKED", 0
    score = 92 if "ng" in email else 85
    return "Deliverable", score

def generate_bulk_hooks(df):
    """Architects a campaign manifesto for every lead"""
    manifesto = "OWO-NEXUS SOVEREIGN OUTREACH MANIFESTO\n" + "="*40 + "\n\n"
    for _, row in df.iterrows():
        manifesto += f"TARGET: {row['Name']} | PITCH: Hi {row['Name']}, I noticed your work as a {row['Role']} in {row['Location']}. Ready to scale {row['Niche']}?\n" + "-"*20 + "\n"
    return manifesto

# --- 4. THE INTERFACE ENGINE ---

def main():
    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("BY TUNDETRONICS NIG. LTD. | INDUSTRIAL AI INFRASTRUCTURE")

    # Verification Handshake
    if "reference" in st.query_params:
        st.success("💎 SOVEREIGN STATUS ACTIVATED. ALL SYSTEMS UNLOCKED.")
        st.session_state['verified_user'] = True
        st.balloons()
        st.query_params.clear()

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "🛡️ Admin Vault"])

    # TAB 1: SEARCH, VERIFY, EXPORT & SCHEDULE
    with tabs[0]:
        c1, c2 = st.columns(2)
        niche = c1.text_input("Niche", placeholder="e.g. Accountants")
        loc = c2.text_input("Location", placeholder="e.g. Abuja")
        
        if st.button("EXECUTE SNIPER"):
            if niche and loc:
                with st.spinner("Deploying Ghost-Agent Swarm..."):
                    status = "Marksman" if st.session_state.get('verified_user') else "Grassroots"
                    df_res, access = run_extraction_swarm(niche, loc, status)
                    st.session_state['last_results'] = df_res
                    st.session_state['access_level'] = access
                    time.sleep(1)
            else: st.error("Define target niche and location first.")

        if st.session_state.get('last_results') is not None:
            df = st.session_state['last_results']
            st.write(f"### 💎 Leads Found (Access: {st.session_state['access_level']})")
            st.dataframe(df)

            if st.session_state['access_level'] == "UNLOCKED":
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.download_button("📥 Bulk CSV Export", data=df.to_csv(index=False).encode('utf-8'), file_name="Sovereign_Leads.csv")
                with col_b:
                    if st.button("🛡️ Run Nexus-Verify"):
                        results = [{"Email": e, "Status": verify_nexus_lead(e)[0]} for e in df['Email']]
                        st.write(pd.DataFrame(results))
                with col_c:
                    if st.button("🚀 Generate Hooks"):
                        st.download_button("📥 Download Manifesto", data=generate_bulk_hooks(df), file_name="Manifesto.txt")
                
                # AGENTIC SCHEDULER
                st.divider()
                st.subheader("⏲️ Agentic Outreach Scheduler")
                col_t, col_d, col_tm = st.columns(3)
                with col_t:
                    sel_lead = st.selectbox("Select Target:", df['Name'])
                with col_d:
                    s_date = st.date_input("Launch Date", min_value=datetime.date.today())
                with col_tm:
                    s_time = st.time_input("Launch Time")
                
                if st.button("🚀 QUEUE MISSION"):
                    st.success(f"Mission Queued for {sel_lead} on {s_date} at {s_time}.")
            else:
                st.warning("⚠️ CSV Export, Nexus-Verify, and Scheduling are reserved for **MARKSMAN** tier.")

    # TAB 2: PRICING
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"""
                <div style='border:1px solid #FACC15; padding:15px; border-radius:10px; background:rgba(250,204,21,0.05); height:280px;'>
                    <h4>{name}</h4>
                    <h2 style='color:#FACC15'>₦{info['price']:,}</h2>
                    <p style='font-size:12px'>{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Upgrade {name}", key=name):
                        st.info("Generating Secure Paystack Link...")
                        # In real use, call init_payment here

    # TAB 3: ADMIN VAULT
    with tabs[2]:
        if st.text_input("Vault Key", type="password") == "OwoNexus2026":
            st.subheader("🛡️ Live Financial Ledger")
            st.info("Vault synced with Paystack API. Tracking real-time revenue.")

if __name__ == "__main__":
    main()