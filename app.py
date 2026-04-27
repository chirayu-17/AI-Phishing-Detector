import streamlit as st
import joblib
import time
from feature_logic import extract_all_features

# Page Config
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="centered")

# Custom CSS for a "Cyber" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_ok_safe=True)

st.title("🛡️ PhishGuard AI")
st.subheader("Enterprise-Grade URL Threat Analysis")

url = st.text_input("Enter URL for deep-scan:", placeholder="https://secure-login-bank.com")

if st.button("🔍 START SECURITY SCAN"):
    with st.status("Analyzing URL structure...", expanded=True) as status:
        # Step 1: Feature Extraction
        features = extract_all_features(url)
        time.sleep(0.5)
        st.write("Checking TLD reputation...")
        
        # Step 2: Prediction
        model = joblib.load("models/phishing_model.pkl")
        # predict_proba gives us the "Confidence %"
        prob = model.predict_proba([features])[0] 
        confidence = round(prob[1] * 100, 2) if prob[1] > prob[0] else round(prob[0] * 100, 2)
        prediction = model.predict([features])[0]
        
        time.sleep(0.5)
        status.update(label="Scan Complete!", state="complete", expanded=False)

    # Display Results
    if prediction == 1:
        st.error(f"🚨 DANGER: HIGH RISK DETECTED ({confidence}% Confidence)")
        st.warning("This URL matches patterns common in Phishing and Social Engineering attacks.")
    else:
        st.success(f"✅ CLEAN: NO THREAT FOUND ({confidence}% Confidence)")
        st.info("The structure of this URL appears consistent with legitimate domains.")

    # Technical Breakdown Expanders
    with st.expander("📊 View Technical Breakdown"):
        col1, col2 = st.columns(2)
        col1.metric("URL Length", features[0])
        col1.metric("Subdomains", features[4])
        col2.metric("HTTPS Enabled", "Yes" if features[7] == 1 else "No")
        col2.metric("Suspicious TLD", "Yes" if features[5] == 1 else "No")