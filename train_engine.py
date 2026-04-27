import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from feature_logic import extract_all_features

# 1. Setup paths
base_path = os.path.dirname(__file__)
# Using 'dataset.csv.csv' as seen in your screenshot
file_path = os.path.join(base_path, "data", "dataset.csv.csv")

print("📂 Loading 235,000+ rows... this will take a few seconds.")
df = pd.read_csv(file_path, low_memory=False)

# 2. Smart Column Detection
# In your file, 'URL' is the second column.
url_col = 'URL' 
# We assume the LAST column is the label (0 or 1).
label_col = df.columns[-1] 

print(f"✅ Using '{url_col}' as Input and '{label_col}' as Target.")

# 3. Clean Data (Remove empty rows)
df = df[[url_col, label_col]].dropna()

# 4. Feature Extraction
# Since the dataset is huge, we will train on the first 50,000 rows 
# to save time. You can increase this once you know it works!
sample_size = 50000 
df_sample = df.sample(n=sample_size, random_state=42)

print(f"🔍 Extracting features from {sample_size} URLs... Please wait.")
X = [extract_all_features(str(u)) for u in df_sample[url_col]]
y = df_sample[label_col]

# 5. Split and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Training the AI... (Using all CPU cores)")
# n_jobs=-1 makes it run faster by using your whole processor
model = RandomForestClassifier(n_estimators=100, n_jobs=-1) 
model.fit(X_train, y_train)

# 6. Evaluate and Save
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"\n📊 Accuracy: {round(accuracy * 100, 2)}%")
print(classification_report(y_test, predictions))

joblib.dump(model, "models/phishing_model.pkl")
print("\n💾 Success! 'models/phishing_model.pkl' is updated and ready.")