import streamlit as st
import pandas as pd
import time

# --- 1. THE SOVEREIGN HOOK LOGIC ---
def generate_roi_hook(name, role, niche):
    """Architects a high-conversion pitch using Sovereign Psychology"""
    hooks = [
        f"Subject: Solving the {niche} Efficiency Gap for {name}\n\nHi {name}, I noticed your work as a {role}. Most in {niche} are losing 20% ROI to manual processes. Our AI Swarm can recover that. Ready to talk?",
        f"Hi {name}, quick question: Is your {niche} firm ready for the 2026 AI shift? As a {role}, you know speed is the only moat. I have a blueprint for you.",
        f"Greetings {name}. Your role as {role} puts you in a unique position to dominate the {niche} market in Nigeria. I've mapped a 10x growth path for you."
    ]
    return hooks[0] # Defaulting to the most industrial hook

# --- 2. INTEGRATING INTO THE UI ---
def main():
    # ... (Previous code remains) ...

    # --- INSIDE TAB 1 (The Swarm) after displaying the dataframe ---
    if st.session_state.get('last_results') is not None:
        st.subheader("🎯 Generate ROI Hooks")
        
        # Create a dropdown to select a specific lead to "Hook"
        df = st.session_state['last_results']
        selected_lead = st.selectbox("Select a Lead to Hook:", df['Name'])
        
        if st.button("GENERATE SOVEREIGN HOOK"):
            lead_data = df[df['Name'] == selected_lead].iloc[0]
            
            with st.spinner(f"Architecting hook for {selected_lead}..."):
                time.sleep(1)
                hook_text = generate_roi_hook(lead_data['Name'], lead_data['Role'], lead_data['Niche'])
                
                st.code(hook_text, language="text")
                st.success("ROI Hook Generated. Copy and Send.")
                st.info("💡 Pro-Tip: Send this via LinkedIn for a 40% higher response rate.")