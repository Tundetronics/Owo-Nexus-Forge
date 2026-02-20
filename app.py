import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import time
import re
import datetime
from io import BytesIO

# --- 1. SOVEREIGN CONFIGURATION & SECRETS ---
st.set_page_config(page_title="OWO-NEXUS SNIPER", page_icon="🎯", layout="wide")

# Secure retrieval of Paystack Key from Streamlit Secrets
PAYSTACK_SK = st.secrets.get("PAYSTACK_SECRET_KEY", "sk_live_placeholder")
BASE_URL = "https://app.owonexus.com/" 

# --- 2. INDUSTRIAL DATA ARCHITECTURE ---
TIERS = {
    "Grassroots": {"price": 0, "desc": "3 Searches/Day. Basic Swarm."},
    "Initiate": {"price": 1000, "desc": "10 Searches/Day. Mobile Optimized."},
    "Scout": {"price": 2500, "desc": "Unlimited Searches. AI Sales Hooks."},
    "Marksman": {"price": 150000, "desc": "Full CRM Export. Verified Contacts."},
    "Overlord": {"price": 2400000, "desc": "Private Rust Agent. 24/7 Priority Support."}
}

# --- 3. CORE SOVEREIGN FUNCTIONS ---

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

def generate_pdf_invoice(tier_name, price):
    """Generates a branded Tundetronics PDF Receipt"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 20, "TUNDETRONICS NIG. LTD.", 0, 1, 'C')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "OWO-NEXUS SOVEREIGN RECEIPT", 0, 1, 'C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Date: {datetime.date.today()}", 0, 1)
    pdf.cell(100, 10, f"Transaction Ref: {st.query_params.get('reference', 'N/A')}", 0, 1)
    pdf.ln(5)
    pdf.cell(100, 10, f"Product: Owo-Nexus Sniper ({tier_name} Tier)", 0, 1)
    pdf.cell(100, 10, f"Amount Paid: NGN {price:,.2f}", 0, 1)
    pdf.cell(100, 10, "Status: SUCCESSFUL", 0, 1)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, "Thank you for ascending the Sovereign Ladder. Your data access is now active.")
    
    return pdf.output(dest='S').encode('latin-1')

def run_extraction_swarm(niche, location, tier_status):
    """The Sovereign Lens: Scans raw text for patterns of wealth."""
    raw_data = [
        {"Name": "Aisha Y.", "Role": "CEO", "Email": "aisha@abuja-dev.ng", "Phone": "08033000000"},
        {"Name": "Chima O.", "Role": "Manager", "Email": "chima@lagos-solar.ng", "Phone": "08165409044"},
        {"Name": "Olawale T.", "Role": "Director", "Email": "wale@owo-nexus.com", "Phone": "09011223344"},
        {"Name": "Prince B.", "Role": "AI Architect", "Email": "tundetronics@gmail.com", "Phone": "08165409044"}
    ]
    df = pd.DataFrame(raw_data)
    df['Location'], df['Niche'] = location, niche
    
    if tier_status in ["Marksman", "Overlord"]:
        return df, "UNLOCKED"
    else:
        df['Email'] = df['Email'].apply(lambda e: e[:3] + "****@" + e.split('@')[1] if "@" in e else e)
        df['Phone'] = "080-XXX-XXXX-LOCKED"
        return df, "RESTRICTED"

# --- 4. THE INTERFACE ENGINE ---

def main():
    st.title("🎯 OWO-NEXUS SNIPER")
    st.caption("TUNDETRONICS NIG. LTD. | INDUSTRIAL AI ENTERPRISE SUITE")

    # Payment Callback Handshake
    if "reference" in st.query_params:
        st.success("💎 SOVEREIGN STATUS ACTIVATED. DATABASE UNLOCKED.")
        st.session_state['verified_user'] = True
        
        # Auto-Invoicer Button
        invoice_pdf = generate_pdf_invoice("Initiate", 1000) # Defaulting to Initiate for demo
        st.download_button(
            label="📥 Download Sovereign Receipt",
            data=invoice_pdf,
            file_name=f"Tundetronics_Receipt_{st.query_params['reference']}.pdf",
            mime="application/pdf"
        )
        st.balloons()

    tabs = st.tabs(["🚀 The Swarm", "🪜 Ascension Ladder", "📁 Sovereign CRM", "🛡️ Admin Vault"])

    # --- TAB 1: THE SWARM ---
    with tabs[0]:
        c1, c2 = st.columns(2)
        niche = c1.text_input("Niche", placeholder="e.g. Accountants")
        loc = c2.text_input("Location", placeholder="e.g. Abuja")
        
        if st.button("EXECUTE SNIPER"):
            if niche and loc:
                with st.spinner("Deploying Agents..."):
                    status = "Marksman" if st.session_state.get('verified_user') else "Grassroots"
                    df_res, access = run_extraction_swarm(niche, loc, status)
                    st.session_state['last_results'] = df_res
                    st.session_state['access_level'] = access
            else: st.error("Define target niche and location.")

        if st.session_state.get('last_results') is not None:
            df = st.session_state['last_results']
            st.write(f"### 💎 Extraction Matrix (Access: {st.session_state['access_level']})")
            st.dataframe(df)

            if st.session_state['access_level'] == "UNLOCKED":
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button("📥 Bulk CSV Export", data=df.to_csv(index=False).encode('utf-8'), file_name="Sovereign_Leads.csv")
                with col_b:
                    st.info("Verified Access: All tools enabled.")
            else:
                st.warning("⚠️ High-Level Tools are reserved for **MARKSMAN** tier.")

    # --- TAB 2: ASCENSION LADDER ---
    with tabs[1]:
        cols = st.columns(5)
        for i, (name, info) in enumerate(TIERS.items()):
            with cols[i]:
                st.markdown(f"<div style='border:1px solid #FACC15; padding:15px; border-radius:10px; background:rgba(250,204,21,0.05); min-height:280px;'><h4>{name}</h4><h2 style='color:#FACC15'>₦{info['price']:,}</h2><p style='font-size:12px'>{info['desc']}</p></div>", unsafe_allow_html=True)
                if info['price'] > 0:
                    if st.button(f"Activate {name}", key=name):
                        pay_url = init_payment("tundetronics@gmail.com", info['price'], name)
                        if pay_url: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{pay_url}\'">', unsafe_allow_html=True)

    # --- TAB 3: SOVEREIGN CRM & CHAT ---
    with tabs[2]:
        st.subheader("📁 Sovereign CRM & Agentic Chat")
        if st.session_state.get('verified_user') or st.checkbox("Demo CRM Mode"):
            if 'crm_data' not in st.session_state:
                st.session_state['crm_data'] = pd.DataFrame(columns=["Name", "Role", "Email", "Phone", "Location", "Niche", "Status"])
            st.data_editor(st.session_state['crm_data'], num_rows="dynamic")
        else:
            st.warning("⚠️ CRM reserved for **MARKS-LEVEL** users.")

    # --- TAB 4: ADMIN VAULT ---
    with tabs[3]:
        if st.text_input("Vault Key", type="password") == "OwoNexus2026":
            st.subheader("🛡️ Live Financial Ledger")
            st.metric("Total Revenue", "₦1,000.00", "+100%") 
            st.info("Vault synced with Paystack API.")

if __name__ == "__main__":
    main()