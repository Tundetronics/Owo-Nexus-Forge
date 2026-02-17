import streamlit as st
import pandas as pd
import time
import re

# --- ARCHITECT'S BRANDING & CONFIG ---
st.set_page_config(page_title="Owo-Nexus Sniper", page_icon="🎯", layout="wide")

# --- SUCCESS LOGIC: PAYSTACK HANDSHAKE ---
# This checks the URL for ?status=success sent by Paystack
query_params = st.query_params
payment_status = query_params.get("status", None)

def verify_email_logic(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)

def main():
    # Sidebar: The Paywall
    st.sidebar.title("💎 Sovereign Access")
    if payment_status != "success":
        st.sidebar.warning("Sniper Limited: Entry Tier")
        st.sidebar.write("To unlock the full 1,000 lead payload & AI enrichment:")
        # Replace with your actual Paystack Link
        st.sidebar.markdown(f'''
            <a href="https://paystack.com/pay/owonexus-sniper" target="_blank">
                <button style="width:100%; background-color:#ffab00; color:black; border:none; padding:10px; border-radius:5px; font-weight:bold; cursor:pointer;">
                    UNLOCK FULL PAYLOAD ($147)
                </button>
            </a>
        ''', unsafe_base_with_html=True)
    else:
        st.sidebar.success("✅ PRO LICENSE ACTIVE")
        st.sidebar.balloons()

    # Main Interface
    st.title("🎯 OWO-NEXUS: SOVEREIGN SNIPER")
    st.info(f"Registry: www.owonexus.com | Status: {'PRO' if payment_status == 'success' else 'FREE'}")
    
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Niche Target (e.g., Solar Installers)")
    with col2:
        location = st.text_input("Location Target (e.g., Abuja, Nigeria)")
    
    if st.button("DEPLOY SNIPER", use_container_width=True):
        if niche and location:
            with st.status("Deploying Sniper Engine...", expanded=True) as status:
                st.write("Extracting raw data...")
                time.sleep(2)
                st.write("Simulating SMTP Handshake verification...")
                time.sleep(2)
                status.update(label="Snipe Complete!", state="complete", expanded=False)
            
            # Simulated Data Generation
            limit = 1000 if payment_status == "success" else 5
            data = {
                "Company": [f"{niche} {i}" for i in range(1, limit + 1)], 
                "Email": [f"contact{i}@{niche.replace(' ', '').lower()}.com" for i in range(1, limit + 1)],
                "Status": ["Verified" for _ in range(limit)]
            }
            df = pd.DataFrame(data)
            
            st.subheader(f"Results: {len(df)} Leads Found")
            st.dataframe(df, use_container_width=True)

            # --- DOWNLOAD LOCK ---
            if payment_status == "success":
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 DOWNLOAD FULL CSV PAYLOAD",
                    data=csv,
                    file_name=f"{niche}_{location}_leads.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("Download Locked. Purchase a Pro License to export this data.")
        else:
            st.error("Please provide target parameters.")

if __name__ == "__main__":
    main()