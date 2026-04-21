import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
texts = [
    
    "hello", "hi", "hey", "good morning",

    
    "bye", "goodbye", "see you",

    
    "thank you", "thanks", "appreciate it",

    
    "i want to travel",
    "plan a trip",
    "book a flight",
    "vacation ideas",

    # tech
    "my computer is broken",
    "i have a bug",
    "tech issue",
    "error on my laptop",

    # university
    "university courses",
    "what should i study",
    "degree options",

    # mental health
    "i feel stressed",
    "i am anxious",
    "need someone to talk to"
]

labels = [
    "greeting","greeting","greeting","greeting",
    "farewell","farewell","farewell",
    "thanks","thanks","thanks",

    "TravelPlanner","TravelPlanner","TravelPlanner","TravelPlanner",

    "TechSupport","TechSupport","TechSupport","TechSupport",

    "UniversityFAQ","UniversityFAQ","UniversityFAQ",

    "MentalHealthSupport","MentalHealthSupport","MentalHealthSupport"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)


model = LogisticRegression()
model.fit(X, labels)


joblib.dump(model, "intent_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model + Vectorizer saved successfully!")