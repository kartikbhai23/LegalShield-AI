import streamlit as st
import time
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="LegalShield AI", page_icon="⚖️", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stTextArea textarea {
        background-color: #1e293b;
        color: white;
        border-radius: 10px;
    }
    .stButton button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HARD-CODED RESPONSES ---
RESPONSES = [
    """### Key Agreements
* You grant a worldwide, non-exclusive license to use your content.
* Subscription fees are non-refundable after the 14-day trial.
* Personal data is shared with affiliates for targeted advertising.
* The service is provided 'as-is' with no liability for data loss.
* Disputes must be settled via individual arbitration.

### Things to Keep in Mind
* The company can modify these terms at any time without notice.
* Inactivity for 6 months leads to permanent account deletion.

### Recommendation
* **Decision:** PROCEED WITH CAUTION
* **Reasoning:** The mandatory arbitration and lack of notification for term changes are high-risk.""",

    """### Key Agreements
* We collect precise GPS location data even when the app is closed.
* Your data may be sold to third-party brokers for marketing.
* You waive your right to participate in class-action lawsuits.
* Automatic renewal applies unless cancelled 48 hours prior.
* Liability for claims is limited to a maximum of $10.00.

### Things to Keep in Mind
* Your private communications are scanned for "policy violations."
* "Growth Partners" is a vague term used for data sharing.

### Recommendation
* **Decision:** DECLINE
* **Reasoning:** Excessive data tracking and extremely low liability caps make this unsafe.""",

    """### Key Agreements
* You retain all ownership rights to the content you upload.
* We use industry-standard encryption for all stored data.
* You can export your data in a machine-readable format anytime.
* Refund requests are honored within a 30-day window.
* Notice of 30 days is provided if the service is discontinued.

### Things to Keep in Mind
* You are responsible for maintaining your own backup of critical files.
* Automated scanning is used only for malware detection.

### Recommendation
* **Decision:** ACCEPT
* **Reasoning:** These terms are user-friendly and align with standard privacy-first practices.""",

    """### Key Agreements
* We reserve the right to increase fees with 7 days' notice.
* Your likeness and username can be used for promotional ads.
* Third-party cookies track your browsing history across the web.
* Accounts can be terminated for "any reason" without explanation.
* Data is stored on servers located outside of your home country.

### Things to Keep in Mind
* The "identity for marketing" clause grants them significant free usage of your brand.
* 7 days for a price hike is significantly shorter than the industry average.

### Recommendation
* **Decision:** PROCEED WITH CAUTION
* **Reasoning:** While functional, the privacy trade-offs and fee structure are slightly aggressive."""
]

# --- UI LAYOUT ---
st.title("⚖️ LegalShield AI")
st.subheader("Summarize complex Terms & Conditions in seconds.")

tc_input = st.text_area("Paste the T&C paragraph here:", height=250, placeholder="By using this service, you agree that...")

if st.button("Summarize"):
    if not tc_input:
        st.error("Please paste some text first!")
    else:
        # 1. Fake "Thinking" states
        status = st.empty()
        
        status.info("🔍 Analyzing legal jargon...")
        time.sleep(1.5)
        
        status.info("🧠 Identifying potential red flags...")
        time.sleep(1.5)
        
        status.info("📝 Drafting summary...")
        time.sleep(1)
        
        status.empty() # Clear status
        
        # 2. Select a random response
        selected_response = random.choice(RESPONSES)
        
        # 3. Simulated Streaming Effect
        placeholder = st.empty()
        full_response = ""
        
        for word in selected_response.split(" "):
            full_response += word + " "
            placeholder.markdown(full_response + "▌")
            time.sleep(0.05) # Adjust speed of streaming here
            
        placeholder.markdown(full_response) # Final render
        st.success("Analysis Complete.")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Gemma 4 E2B (Simulated) | Built for CSE-AIML 2026 Projects")