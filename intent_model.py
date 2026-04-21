import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Dummy training data (replace later)
texts = [
    "hello",
    "hi",
    "bye",
    "goodbye",
    "thanks",
    "thank you"
]

labels = [
    "greeting",
    "greeting",
    "farewell",
    "farewell",
    "thanks",
    "thanks"
]

# Train
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

# Save BOTH
joblib.dump((model, vectorizer), "intent_model.pkl")

print("intent_model.pkl created")