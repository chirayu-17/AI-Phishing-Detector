import streamlit as st
import joblib
import time
import os
from feature_logic import extract_all_features

# 1. Page Configuration
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="centered")

# 2. Professional "Cyber" Styling (Fixes the previous TypeError)
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
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.title("🛡️ PhishGuard AI")
st.subheader("Enterprise-Grade URL Threat Analysis")
st.write("Analyze links in real-time using our trained Machine Learning engine.")

# 4. Load the Trained Model
# We use a try-except block to handle cases where the file isn't found
model_path = os.path.join("models", "phishing_model.pkl")
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error("⚠️ Model file not found. Please run 'train_engine.py' first.")
    st.stop()

# 5. User Input
target_url = st.text_input("Paste URL for deep-scan:", placeholder="https://secure-login-portal.com")

# 6. Scan Logic
if st.button("🔍 START SECURITY SCAN"):
    if target_url:
        with st.status("Initializing Neural Engine...", expanded=True) as status:
            # Feature Extraction
            st.write("Extracting URL metadata...")
            features = extract_all_features(target_url)
            time.sleep(0.4)
            
            # Prediction Logic
            st.write("Running heuristic analysis...")
            # We use predict_proba to get the confidence percentage
            probabilities = model.predict_proba([features])[0]
            prediction = model.predict([features])[0]
            
            # Calculate Confidence based on the predicted class
            confidence = round(probabilities[prediction] * 100, 2)
            
            time.sleep(0.4)
            status.update(label="Scan Complete!", state="complete", expanded=False)

        # 7. Results Display
        st.divider()
        if prediction == 1:
            st.error(f"🚨 DANGER: HIGH RISK DETECTED ({confidence}% Confidence)")
            st.markdown("### Threat Assessment")
            st.write("This URL exhibits patterns highly consistent with **Phishing** and **Credential Harvesting** sites.")
        else:
            st.success(f"✅ CLEAN: NO THREAT FOUND ({confidence}% Confidence)")
            st.markdown("### Safety Assessment")
            st.write("The structural analysis indicates this URL is likely **Legitimate** and safe to visit.")

        # 8. Technical Breakdown metrics
        with st.expander("📊 View Forensic Data"):
            col1, col2 = st.columns(2)
            col1.metric("URL Length", features[0])
            col1.metric("Subdomain Depth", features[4])
            col2.metric("HTTPS Protocol", "Secure" if features[7] == 1 else "Insecure")
            col2.metric("Suspicious TLD", "Yes" if features[5] == 1 else "No")
    else:
        st.warning("Please enter a URL to begin the scan.")

# 9. Footer
st.divider()
st.caption("Developed by Chirayu Patil ")