import streamlit as st
import joblib
import time
import os
import tldextract
from feature_logic import extract_all_features

# 1. Page Configuration
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="centered")

# 2. Professional "Cyber" Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        background-color: #ff4b4b; 
        color: white; 
        font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Global Whitelist (Reputation Layer)
# Add any trusted domains here to prevent false positives
WHITELIST = [
    "google.com", "amazon.com", "amazon.in", "hackthebox.com", 
    "github.com", "microsoft.com", "apple.com", "linkedin.com",
    "netflix.com", "instagram.com", "twitter.com", "gmail.com",
    "youtube.com", "stackoverflow.com", "streamlit.io"
]

def is_whitelisted(url):
    ext = tldextract.extract(url)
    root_domain = f"{ext.domain}.{ext.suffix}"
    return root_domain.lower() in WHITELIST

# 4. Header Section
st.title("🛡️ PhishGuard AI")
st.subheader("Enterprise-Grade URL Threat Analysis")

# 5. Load the Trained Model
model_path = os.path.join("models", "phishing_model.pkl")
try:
    model = joblib.load(model_path)
except Exception:
    st.error("⚠️ Model file not found. Please run 'train_engine.py' first.")
    st.stop()

# 6. User Input
target_url = st.text_input("Paste URL for deep-scan:", placeholder="https://secure-login-portal.com")

# 7. Scan Logic
if st.button("🔍 START SECURITY SCAN"):
    if target_url:
        with st.status("Analyzing URL Architecture...", expanded=True) as status:
            # Step A: Check Whitelist (Reputation Layer)
            if is_whitelisted(target_url):
                final_prediction = 0
                confidence = 100.0
                reason = "Verified Reputation (Global Whitelist)"
                features = extract_all_features(target_url) # Still extract for the forensic view
            else:
                # Step B: Extract Features
                st.write("Extracting forensic metadata...")
                features = extract_all_features(target_url)
                
                # Step C: Heuristic Override (Tunneling Check)
                is_high_risk_tunnel = features[8] == 1 # is_tunneled
                
                if is_high_risk_tunnel:
                    final_prediction = 1
                    confidence = 100.0
                    reason = "Tunneling Service Detected (High Risk Bypass)"
                else:
                    # Step D: AI Analysis
                    st.write("Running Neural Engine analysis...")
                    probabilities = model.predict_proba([features])[0]
                    ai_prediction = model.predict([features])[0]
                    final_prediction = ai_prediction
                    confidence = round(probabilities[final_prediction] * 100, 2)
                    reason = "Machine Learning Pattern Analysis"

            time.sleep(0.5)
            status.update(label="Scan Complete!", state="complete", expanded=False)

        # 8. Results Display
        st.divider()
        if final_prediction == 1:
            st.error(f"🚨 DANGER: HIGH RISK DETECTED ({confidence}%)")
            st.warning(f"**Threat Assessment:** {reason}")
            st.write("This URL exhibits patterns highly consistent with Phishing attacks.")
        else:
            st.success(f"✅ CLEAN: NO THREAT FOUND ({confidence}%)")
            st.info(f"**Safety Assessment:** {reason}")

        # 9. Forensic Data Display
        with st.expander("📊 View Forensic Data"):
            col1, col2 = st.columns(2)
            col1.metric("URL Length", features[0])
            col1.metric("Subdomain Depth", features[4])
            col1.metric("Tunneling Service", "DETECTED" if features[8] == 1 else "None")
            
            col2.metric("HTTPS Protocol", "Secure" if features[5] == 1 else "Insecure")
            col2.metric("Suspicious TLD", "Yes" if features[6] == 1 else "No")
            col2.metric("Keyword Flag", "Found" if features[9] == 1 else "Clean")
    else:
        st.warning("Please enter a URL to begin the scan.")

st.divider()
st.caption("Developed by Chirayu Patil | Layered Defense: Reputation + Heuristics + AI")