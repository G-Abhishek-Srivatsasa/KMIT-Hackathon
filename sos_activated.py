import streamlit as st
import time # Added for simulating a check

def display_sos_activated():
    # ---------- PAGE CONFIG & CUSTOM CSS (Kept the original background) ----------
    st.set_page_config(page_title="SOS Alert", page_icon="🚨", layout="centered")
    st.markdown("""
<style>
/* Main app background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 20%, #0a192f 0%, #122c56 90%);
}

/* Custom CSS for the SOS Title */
@keyframes pulse {
    0% { color: #FF4B4B; text-shadow: 0 0 5px #FF4B4B; }
    50% { color: #FF0000; text-shadow: 0 0 20px #FF0000, 0 0 30px rgba(255, 0, 0, 0.7); }
    100% { color: #FF4B4B; text-shadow: 0 0 5px #FF4B4B; }
}

.sos-title {
    font-size: 60px;
    font-weight: 900;
    text-align: center;
    margin-top: 50px;
    margin-bottom: 30px;
    animation: pulse 1s infinite alternate; /* Apply the pulse animation */
}

/* Subtext for the help message */
.help-message {
    color: #F8F9FA;
    font-size: 24px;
    text-align: center;
    margin-bottom: 40px;
}

/* Card style for status updates */
.status-card {
    background-color: rgba(255, 75, 75, 0.1); /* Light red background */
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #FF4B4B; /* Red border */
    box-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
    text-align: center;
    color: #FFDDDD;
}
.status-header {
    font-size: 30px;
    color: #FF4B4B;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
    
    # Use HTML for the main title with pulsating red color
    st.markdown("<h1 class='sos-title'> SOS Activated </h1>", unsafe_allow_html=True)
    
    # Display the primary message with a cool, reassuring tone
    st.markdown("<p class='help-message'>Your location and current status have been transmitted.</p>", unsafe_allow_html=True)

    # Status update section
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.markdown("<p class='status-header'>Status Update</p>", unsafe_allow_html=True)
    
    status_placeholder = st.empty()
    
    # Simulate the steps for contacting help
    status_placeholder.info("Establishing secure connection with emergency contacts...")
    time.sleep(2)
    
    status_placeholder.warning("Contacting nearest police station and pre-set emergency contacts...")
    time.sleep(2)
    
    # Final message that help is confirmed
    status_placeholder.success("✅ **CONFIRMED:** Help is being dispatched and contacts have been notified. Stay safe!")
    
    
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    display_sos_activated()