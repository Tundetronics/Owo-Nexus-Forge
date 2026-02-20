import streamlit as st
import pandas as pd
import time

# --- 1. THE BULK HOOK ENGINE ---
def generate_bulk_hooks(df):
    """Architects a campaign manifesto for every lead in the dataframe"""
    manifesto = "OWO-NEXUS SOVEREIGN OUTREACH MANIFESTO\n"
    manifesto += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    manifesto += "="*40 + "\n\n"
    
    for _, row in df.iterrows():
        hook = f"TARGET: {row['Name']} ({row['Role']})\n"
        hook += f"NICHE: {row['Niche']} | {row['Location']}\n"
        hook += f"PITCH: Hi {row['Name']}, I noticed your work as a {row['Role']} in {row['Location']}. "
        hook += f"Most in {row['Niche']} are losing ROI to manual processes. Ready to scale?\n"
        hook += "-"*20 + "\n"
        manifesto += hook
        
    return manifesto

# --- 2. UPDATING THE UI IN TAB 1 ---
def main():
    # ... (Previous code remains) ...

    if st.session_state.get('last_results') is not None:
        df = st.session_state['last_results']
        status = "Marksman" if st.session_state.get('verified_user') else "Grassroots"
        
        st.divider()
        st.subheader("🎯 Sovereign Hook Center")
        
        # --- THE BULK OPTION (MARKSMAN ONLY) ---
        if status in ["Marksman", "Overlord"]:
            st.info("💎 MARKS-LEVEL ACCESS: Bulk Generation Enabled.")
            if st.button("🚀 GENERATE BULK MANIFESTO"):
                with st.spinner("Architecting Campaign..."):
                    time.sleep(2)
                    manifesto_text = generate_bulk_hooks(df)
                    
                    st.download_button(
                        label="📥 Download Outreach Manifesto",
                        data=manifesto_text,
                        file_name=f"Sovereign_Manifesto_{int(time.time())}.txt",
                        mime="text/plain"
                    )
                    st.success("Manifesto Ready. Your swarm is prepared for deployment.")
        else:
            # Individual Hook (The "Tease" for lower tiers)
            selected_lead = st.selectbox("Select a Lead to Hook:", df['Name'])
            if st.button("Generate Single Hook"):
                # (Previous single hook logic)
                st.warning("Bulk generation is reserved for **MARKSMAN** tier.")