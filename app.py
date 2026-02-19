import streamlit as st
import pandas as pd
import time
import re

# --- ADD THIS TO YOUR UTILITIES SECTION ---
def convert_df_to_csv(df):
    """Encodes the dataframe into a CSV for Sovereign Export"""
    return df.to_csv(index=False).encode('utf-8')

# --- UPDATED EXTRACTION LOGIC ---
def run_extraction_swarm(niche, location, tier_status):
    # Simulated Raw Search Data
    raw_data = [
        {"Name": "Aisha Y.", "Role": "CEO", "Email": "aisha@abuja-dev.ng", "Phone": "08033000000"},
        {"Name": "Chima O.", "Role": "Manager", "Email": "chima@lagos-solar.ng", "Phone": "08165409044"},
        {"Name": "Olawale T.", "Role": "Director", "Email": "wale@owo-nexus.com", "Phone": "09011223344"}
    ]
    
    df = pd.DataFrame(raw_data)
    df['Location'] = location
    df['Niche'] = niche
    
    if tier_status in ["Marksman", "Overlord"]:
        return df, "UNLOCKED"
    else:
        # Masking for FOMO
        df['Email'] = df['Email'].apply(lambda e: e[:3] + "****@" + e.split('@')[1])
        df['Phone'] = "080-XXX-XXXX-LOCKED"
        return df, "RESTRICTED"

# --- INSIDE TAB 1 (The Swarm) ---
with tabs[0]:
    st.subheader("Deploy Ghost-Agent Swarm")
    niche = st.text_input("Niche", placeholder="e.g. Solar Engineers")
    loc = st.text_input("Location", placeholder="e.g. Lagos")
    
    if st.button("EXECUTE SNIPER"):
        if niche and loc:
            with st.spinner("Extracting High-Intent Leads..."):
                status = "Marksman" if st.session_state.get('verified_user') else "Grassroots"
                df_results, access_level = run_extraction_swarm(niche, loc, status)
                time.sleep(1)
                
                st.write(f"### 💎 Extracted Leads Status: {access_level}")
                st.dataframe(df_results)
                
                # --- THE EXPORT GATE ---
                if access_level == "UNLOCKED":
                    csv_data = convert_df_to_csv(df_results)
                    st.download_button(
                        label="📥 Download Bulk CSV",
                        data=csv_data,
                        file_name=f"Sovereign_Leads_{niche}_{loc}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("⚠️ Bulk CSV Export is reserved for **MARKSMAN** tier.")