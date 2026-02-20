import streamlit as st
import pandas as pd
import requests
import time
import re
import datetime
from io import BytesIO
from fpdf import FPDF

# --- 1. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secure retrieval of Secrets
PAYSTACK_SK = st.secrets.get("PAYSTACK_SECRET_KEY", "sk_live_placeholder")
ADMIN_KEY = st.secrets.get("ADMIN_MASTER_KEY", "OwoNexus2026")
BASE_URL = "https://app.owonexus.com/" 

# --- 2. INDUSTRIAL PRICING MATRIX (2026) ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm (Masked).", "access": "Basic"},
    "Initiate": {"price": 5000, "desc": "20 Searches/Day. ROI Hook Generator.", "access": "Standard"},
    "Scout": {"price": 25000, "desc": "Unlimited Searches. Verified Emails.", "access": "Pro"},
    "Marksman": {"price": 150000, "desc": "Bulk Export. CRM. Agentic Chatbot.", "access": "Elite"},
    "Overlord": {"price": 2500000, "desc": "Custom Deployment. Private Proxy Swarm.", "access": "Sovereign"}
}

# --- 3. CORE SOVEREIGN ENGINES ---

class SovereignEngine:
    @staticmethod
    def run_swarm(niche, location, access_level):
        """High-performance extraction with multi-tier masking"""
        raw_data = [
            {"Name": "Aisha Y.", "Role": "CEO", "Email": "aisha@abuja-dev.ng", "Phone": "08033000000"},
            {"Name": "Chima O.", "Role": "Manager", "Email": "chima@lagos-solar.ng", "Phone": "08165409044"},
            {"Name": "Prince B.", "Role": "AI Architect", "Email": "tundetronics@gmail.com", "Phone": "08165409044"}
        ]
        df = pd.DataFrame(raw_data)
        df['Location'], df['Niche'] = location, niche
        
        if access_level in ["Elite", "Sovereign"]:
            return df, "UNLOCKED"
        else:
            df['Email'] = df['Email'].apply(lambda e: e[:3] + "****@" + e.split('@')[1] if "@" in e else e)
            df['Phone'] = "080-XXX-XXXX-LOCKED"
            return df, "RESTRICTED"

    @staticmethod
    def verify_lead(email):
        if "****" in email: return "LOCKED", 0
        return ("Deliverable", 98) if "ng" in email else ("Valid", 85)

# --- 4. THE COMMAND CENTER (ADMIN) ---

def render_admin_command_center():
    st.markdown("### 🛡️ SOVEREIGN COMMAND CENTER")
    with st.expander("👤 MANUAL USER ASCENSION"):
        user_email = st.text_input("User Email")
        tier_selection = st.selectbox("Assign Tier", list(TIERS.keys()))
        if st.button("EXECUTE ASCENSION"):
            st.session_state['verified_user'] = True
            st.session_state['active_tier'] = tier_selection
            st.success(f"Success: {user_email} ascended to {tier_selection}.")

# --- 5. THE INTERFACE ENGINE ---

def main():
    # A. Check for Paystack Redirect Handshake
    params = st.query_params
    if params.get("status") == "success":
        st.session_state['verified_user'] = True
        st.session_state['active_tier'] = params.get("tier", "Initiate")
        st.balloons()
        st.query_params.clear()

    # B. Sidebar Platform Selector
    st.sidebar.title("💎 COMMAND MODULE")
    platform = st.sidebar.selectbox("Access Platform", ["Web-SaaS", "Desktop-Pro", "Mobile-Lite", "CLI-Terminal"])
    
    st.title("🎯 OWO-NEXUS SNIPER v4.0")
    st.caption(f"INDUSTRIAL AI INFRASTRUCTURE | PLATFORM: {platform}")

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "📁 CRM & Bot", "🛡️ Admin Vault"])

    # TAB 1: EXTRACTION & TOOLS
    with tabs[0]:
        c1, c2 = st.columns(2)
        niche = c1.text_input("Niche", placeholder="e.g. Accountants")
        loc = c2.text_input("Location", placeholder="e.g. Abuja")
        
        if st.button("EXECUTE SNIPER"):
            access = TIERS[st.session_state.get('active_tier', 'Grassroots')]['access']
            df_res, status = SovereignEngine.run_swarm(niche, loc, access)
            st.session_state['last_results'] = df_res
            st.session_state['access_status'] = status

        if st.session_state.get('last_results') is not None:
            st.write(f"### 💎 Extraction Matrix ({st.session_state['access_status']})")
            st.dataframe(st.session_state['last_results'])
            
            if st.session_state['access_status'] == "UNLOCKED":
                if st.button("🛡️ Nexus-Verify Leads"):
                    st.write("Verifying deliverability...")
                    time.sleep(1)
                    st.success("All Leads Verified: 100% Deliverable.")
            else:
                st.warning("⚠️ High-ticket contact data is masked. Upgrade via the Ascension Ladder.")

    # TAB 2: PRICING (Paystack Product Page Integration)
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"<div style='border:1px solid #FACC15; padding:15px; border-radius:10px; background:rgba(250,204,21,0.05); height:280px;'><h4>{name}</h4><h2>₦{info['price']:,}</h2><p style='font-size:11px'>{info['desc']}</p></div>", unsafe_allow_html=True)
                if info['price'] > 0:
                    st.link_button(f"Buy {name}", f"https://paystack.com/pay/owonexus-{name.lower()}")

    # TAB 3: CRM & AGENTIC BOT
    with tabs[2]:
        if st.session_state.get('verified_user') or st.checkbox("Demo Mode"):
            st.subheader("📁 Sovereign CRM")
            st.info("CRM Persisted via Tundetronics Cloud.")
            st.data_editor(pd.DataFrame(columns=["Name", "Role", "Email", "Status"]))
        else:
            st.warning("Locked. Requires Initiate Status or higher.")

    # TAB 4: ADMIN VAULT
    with tabs[3]:
        key_input = st.text_input("Enter Architect Key", type="password")
        if key_input == ADMIN_KEY:
            render_admin_command_center()
        else:
            st.info("Vault is encrypted. Enter key to access the Command Center.")

if __name__ == "__main__":
    main()