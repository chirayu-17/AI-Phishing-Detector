import streamlit as st
import joblib
from feature_logic import extract_all_features

# Setup the page look
st.set_page_config(page_title="AI Phish Guard", page_icon="🛡️")
st.title("🛡️ AI-Powered Phishing Link Detector")
st.markdown("Enter a URL below to analyze it using our trained Machine Learning model.")

# Load the "brain" we created in Step 4
try:
    model = joblib.load("models/phishing_model.pkl")
except:
    st.error("Error: Trained model not found. Run 'train_engine.py' first!")

# Create the input box
target_url = st.text_input("Paste URL here:", placeholder="https://example.com")

if st.button("Run Security Scan"):
    if target_url:
        # 1. Transform the input into the same 5 numbers we used for training
        numeric_features = extract_all_features(target_url)
        
        # 2. Predict (The model returns [0] or [1])
        prediction = model.predict([numeric_features])[0]
        
        # 3. Display Result
        if prediction == 1:
            st.error("🚨 DANGER: This URL exhibits phishing characteristics!")
        else:
            st.success("✅ SAFE: This URL appears to be legitimate.")
            
        # Optional: Show the technical breakdown
        with st.expander("See technical analysis"):
            st.write(f"URL Length: {numeric_features[0]}")
            st.write(f"Has '@' symbol: {'Yes' if numeric_features[1] == 1 else 'No'}")
            st.write(f"Dot count: {numeric_features[2]}")
    else:
        st.warning("Please enter a URL to analyze.")