# 🛡️ PhishGuard AI: Machine Learning URL Detector

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A high-performance cybersecurity tool that uses Machine Learning to detect phishing URLs in real-time. By analyzing the "DNA" of a URL, this tool identifies malicious patterns before a user clicks.

🔗 **[Live Demo: Try PhishGuard AI Here]((https://rayu-phish-guard.streamlit.app/))**

---

## 📊 Performance Metrics
The model was trained on a balanced dataset of **50,000+ real-world URLs**, achieving enterprise-grade detection rates:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **94.17%** |
| **Recall (Phishing)** | **0.98** |
| **F1-Score** | **0.95** |

*The high Recall score (0.98) ensures that 98% of actual phishing threats are successfully intercepted.*

---

## 🚀 Key Features
- **Real-Time Analysis:** Instant scan results using a pre-trained Random Forest model.
- **Forensic Breakdown:** View URL metadata including length, subdomain depth, and protocol status.
- **Heuristic Detection:** Identifies suspicious TLDs (e.g., .xyz, .tk) and character patterns (e.g., '@', hyphens).
- **Confidence Scoring:** Displays the AI's certainty for every scan result.

---

## 🛠️ Tech Stack
- **Backend:** Python
- **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, Joblib
- **Feature Extraction:** TLDextract, Regular Expressions (re)
- **Frontend/Deployment:** Streamlit Cloud

---

## 📂 Project Structure
```text
├── app.py                # Streamlit Web Interface
├── feature_logic.py      # URL Feature Extraction Logic
├── train_engine.py       # ML Training Script
├── models/
│   └── phishing_model.pkl # The Trained AI "Brain"
├── data/
│   └── dataset.csv       # Training Data (Ignored by Git)
└── requirements.txt      # Dependencies
