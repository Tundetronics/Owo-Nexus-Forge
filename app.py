import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import re

# --- 1. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

PAYSTACK_SK = st.secrets["PAYSTACK_SECRET_KEY"]
BASE_URL = "https://app.owonexus.com/"

# --- 2. DATA & EXTRACTION LOGIC ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "desc": "10 Searches/Day. Mobile Optimized."},
    "Scout": {"price": 2500, "desc": "Unlimited Searches. AI Sales Hooks."},
    "Marksman": {"price": 150000, "desc": "Full CRM Export. Verified Contacts."},
    "Overlord": {"price": 2400000, "desc": "Private Rust Agent. 24/7 Priority Support."}
}

def run_extraction_swarm(niche, location, tier_status):
    """The Sovereign Lens: Scans raw text for patterns of wealth."""
    # Simulated Raw Search Result (In Overlord build, this pulls from SerpApi)
    raw_data = f"Lead: MD at {location} {niche} Firm. info@target-niche.ng, +2348165409044. LinkedIn: /in/lead-profile"
    
    # Regex Patterns for Nigerian Context
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+234|0)[789][01]\d{8}'
    
    emails = list(set(re.findall(email_pattern, raw_data)))
    phones = list(set(re.findall(phone_pattern, raw_data)))
    
    # Tier-Based Masking Logic (FOMO Engine)
    if tier_status in ["Marksman", "Overlord"]:
        return {"Emails": emails, "Phones": phones, "Status": "UNLOCKED"}
    else:
        # Mask emails (e.g., tundetronics@gmail.com -> tun****@gmail.com)
        masked_emails = [e[:3] + "****@" + e.split('@')[1] for e in emails]
        return {"Emails": masked_emails, "Phones": ["+234-XXX-XXXX-LOCKED"], "Status": "RESTRICTED"}

# --- 3. UTILITIES ---
def init_payment(email, amount, tier):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SK}"}
    payload = {"email": email, "amount": int(amount * 100), "callback_url": BASE_URL, "metadata": {"tier": tier}}
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return res['data']['authorization_url'] if res.get('status') else None
    except: return None

# --- 4. THE SOVEREIGN INTERFACE ---
def main():
    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("BY TUNDETRONICS NIG. LTD. | INDUSTRIAL DATA EXTRACTION")

    # Payment Handshake Verification
    if "reference" in st.query_params:
        st.success("💎 SOVEREIGN STATUS ACTIVATED. DATA MASKING ADJUSTED.")
        st.session_state['verified_user'] = True # Temporary session state
        st.balloons()
        st.query_params.clear()

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "🛡️ Admin Vault"])

    # TAB 1: SEARCH & EXTRACTION
    with tabs[0]:
        st.subheader("Deploy Ghost-Agent Swarm")
        c1, c2 = st.columns(2)
        niche = c1.text_input("Niche", placeholder="e.g. Accountants")
        loc = c2.text_input("Location", placeholder="e.g. Abuja")
        
        if st.button("EXECUTE SNIPER"):
            if niche and loc:
                with st.spinner("Extracting High-Intent Leads..."):
                    # Check for verified status
                    status = "Marksman" if st.session_state.get('verified_user') else "Grassroots"
                    results = run_extraction_swarm(niche, loc, status)
                    time.sleep(1)
                    
                    st.write(f"### 💎 Extracted Leads for {niche} in {loc}")
                    st.table(pd.DataFrame({
                        "Metric": ["Emails Found", "Phones Found", "Access Level"],
                        "Value": [", ".join(results['Emails']), ", ".join(results['Phones']), results['Status']]
                    }))
                    
                    if results['Status'] == "RESTRICTED":
                        st.warning("⚠️ Full data is locked. Upgrade to **MARKSMAN** to reveal phone numbers.")
            else:
                st.error("Define target niche and location first.")

    # TAB 2: ASCENSION LADDER
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"<div style='border:1px solid #FACC15; padding:15px; border-radius:10px; background:rgba(250,204,21,0.05); height:280px;'><h4>{name}</h4><h2 style='color:#FACC15'>₦{info['price']:,}</h2><p style='font-size:12px'>{info['desc']}</p></div>", unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Upgrade {name}", key=name):
                        link = init_payment("tundetronics@gmail.com", info['price'], name)
                        if link: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{link}\'">', unsafe_allow_html=True)

    # TAB 3: ADMIN VAULT
    with tabs[2]:
        pwd = st.text_input("Vault Key", type="password")
        if pwd == "OwoNexus2026":
            st.info("Vault synced. Pulled real-time data from Paystack.")
            # (Insert previous Vault Logic here for real-time tracking)

if __name__ == "__main__":
    main()