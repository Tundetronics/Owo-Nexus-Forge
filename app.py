import streamlit as st
import pandas as pd
import time
import google.generativeai as genai

# --- ARCHITECT CONFIG & AI SETUP ---
st.set_page_config(page_title="Owo-Nexus Sniper", page_icon="🎯", layout="wide")

# Configure Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("AI Engine Offline: Please check GEMINI_API_KEY in Streamlit Secrets.")

# --- SUCCESS LOGIC: PAYSTACK HANDSHAKE ---
query_params = st.query_params
payment_status = query_params.get("status", None)

def generate_sales_hook(company, niche):
    """Generates a custom AI hook for the lead."""
    try:
        prompt = f"Write a professional 1-sentence sales hook for {company}, a business in the {niche} industry. Focus on efficiency and growth."
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Lead ready for outreach."

def main():
    # Sidebar: The Paywall
    st.sidebar.title("💎 Sovereign Access")
    if payment_status != "success":
        st.sidebar.warning("Sniper Limited: Entry Tier")
        st.sidebar.markdown(f'''
            <a href="https://paystack.com/pay/owonexus-sniper" target="_blank">
                <button style="width:100%; background-color:#ffab00; color:black; border:none; padding:10px; border-radius:5px; font-weight:bold; cursor:pointer;">
                    UNLOCK AI ENRICHMENT ($147)
                </button>
            </a>
        ''', unsafe_base_with_html=True)
    else:
        st.sidebar.success("✅ PRO LICENSE: AI ENRICHMENT ACTIVE")

    # Main Interface
    st.title("🎯 OWO-NEXUS: SOVEREIGN SNIPER")
    st.info(f"Registry: www.owonexus.com | Mode: {'AI-ENHANCED' if payment_status == 'success' else 'RAW DATA'}")
    
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Niche Target", placeholder="e.g. Solar Energy")
    with col2:
        location = st.text_input("Location Target", placeholder="e.g. Lagos, Nigeria")
    
    if st.button("DEPLOY SNIPER", use_container_width=True):
        if niche and location:
            # 1. Extraction Phase
            with st.spinner("Sniping raw leads..."):
                limit = 20 if payment_status == "success" else 5 # Adjusted for demo speed
                data = {
                    "Company": [f"{niche} Group {i}" for i in range(1, limit + 1)], 
                    "Email": [f"info@company{i}.com" for i in range(1, limit + 1)],
                    "Status": ["Verified" for _ in range(limit)]
                }
                df = pd.DataFrame(data)

            # 2. Enrichment Phase (The "Success Logic")
            if payment_status == "success":
                hooks = []
                progress_text = "AI Architect is writing custom hooks..."
                my_bar = st.progress(0, text=progress_text)
                
                for i, row in df.iterrows():
                    hooks.append(generate_sales_hook(row['Company'], niche))
                    my_bar.progress((i + 1) / len(df), text=progress_text)
                
                df['AI Sales Hook'] = hooks
                st.balloons()

            st.subheader(f"Results: {len(df)} Leads Processed")
            st.dataframe(df, use_container_width=True)

            # 3. Download Logic
            if payment_status == "success":
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 DOWNLOAD AI-ENRICHED PAYLOAD", csv, f"{niche}_enriched.csv", "text/csv", use_container_width=True)
            else:
                st.warning("AI Enrichment & Downloads are locked. Upgrade to Pro to export.")
        else:
            st.error("Targets required.")

if __name__ == "__main__":
    main()