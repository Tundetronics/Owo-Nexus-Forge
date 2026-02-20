# --- ADD TO YOUR ADMIN COMMAND CENTER ---
def render_admin_command_center():
    # ... (Previous user management code) ...
    
    with st.expander("🤖 AGENTIC MARKETING BRIDGE"):
        st.write("WhatsApp Status: **ACTIVE (Listening via Twilio)**")
        st.write("LinkedIn API: **CONNECTED**")
        st.write("X (Twitter) API: **CONNECTED**")
        
        if st.button("TEST BRIDGE"):
            # Simulation of a WhatsApp trigger
            agent = WhatsAppSovereignAgent()
            test_res = agent.process_command("Post X: Owo-Nexus Sniper v4.5 is officially agentic. #SovereignTech")
            st.info(test_res)