import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from feature_logic import extract_all_features

# 1. Read your data
# This uses the 'Pandas' library to open the CSV file
df = pd.read_csv("data/dataset.csv")

# 2. The "Loop"
# For every URL in your CSV, run our feature function and store it in 'X'
print("Starting feature extraction...")
X = []
for url in df['url']:
    features = extract_all_features(str(url))
    X.append(features)

# 3. The "Labels"
# 'y' is the answer key (0 = safe, 1 = phishing)
y = df['label']

# 4. Initialize the Model
# RandomForest is like a group of decision trees voting on the answer.
model = RandomForestClassifier(n_estimators=100)

# 5. The Training Phase
# This is where the computer learns patterns between URL features and the label.
print("Training the AI... please wait.")
model.fit(X, y)

# 6. Save the Result
# We save this "trained brain" so we don't have to train it every time we use it.
joblib.dump(model, "models/phishing_model.pkl")
print("Success! Model saved in models/phishing_model.pkl")