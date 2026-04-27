import streamlit as st
import joblib
import time
import os
from feature_logic import extract_all_features

# Page Config
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="centered")

# Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PhishGuard AI")
st.subheader("Enterprise-Grade URL Threat Analysis")

# Load Model
model_path = os.path.join("models", "phishing_model.pkl")
try:
    model = joblib.load(model_path)
except:
    st.error("⚠️ Model not found.")
    st.stop()

target_url = st.text_input("Paste URL for deep-scan:", placeholder="https://secure-login-portal.com")

if st.button("🔍 START SECURITY SCAN"):
    if target_url:
        with st.status("Analyzing URL Architecture...", expanded=True) as status:
            features = extract_all_features(target_url)
            
            # --- SECURITY OVERRIDE LAYER (Heuristics) ---
            # features[8] is 'is_tunneled'
            # features[9] is 'has_keyword'
            is_high_risk_tunnel = features[8] == 1
            is_brand_impersonation = features[9] == 1
            
            # AI Prediction
            probabilities = model.predict_proba([features])[0]
            ai_prediction = model.predict([features])[0]
            
            # Logic: If it's a tunnel, it's DANGER (Override AI)
            if is_high_risk_tunnel:
                final_prediction = 1
                confidence = 100.0
                reason = "Tunneling Service Detected (High Risk Bypass)"
            else:
                final_prediction = ai_prediction
                confidence = round(probabilities[final_prediction] * 100, 2)
                reason = "Machine Learning Pattern Analysis"

            time.sleep(0.6)
            status.update(label="Scan Complete!", state="complete", expanded=False)

        # Display Results
        st.divider()
        if final_prediction == 1:
            st.error(f"🚨 DANGER: HIGH RISK DETECTED ({confidence}%)")
            st.warning(f"Reason: {reason}")
        else:
            st.success(f"✅ CLEAN: NO THREAT FOUND ({confidence}%)")

        # Fixed Forensic Data (Matching the 10 features in order)
        with st.expander("📊 View Forensic Data"):
            col1, col2 = st.columns(2)
            col1.metric("URL Length", features[0])
            col1.metric("Subdomain Depth", features[4])
            col1.metric("Tunneling Service", "DETECTED" if features[8] == 1 else "None")
            
            col2.metric("HTTPS Protocol", "Secure" if features[5] == 1 else "Insecure")
            col2.metric("Suspicious TLD", "Yes" if features[6] == 1 else "No")
            col2.metric("Keyword Flag", "Found" if features[9] == 1 else "Clean")
    else:
        st.warning("Please enter a URL.")