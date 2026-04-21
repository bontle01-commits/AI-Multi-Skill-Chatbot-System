import joblib
import os


class Chatbot:
    def __init__(self, skills):
        self.skills = skills

        model_path = "intent_model.pkl"
        vectorizer_path = "vectorizer.pkl"

        if not os.path.exists(model_path):
            raise FileNotFoundError("Missing intent_model.pkl")

        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError("Missing vectorizer.pkl")

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def detect_intent(self, user_input: str):
        user_input = user_input.lower().strip()
        X = self.vectorizer.transform([user_input])
        intent = self.model.predict(X)[0]

        print("DEBUG INTENT:", intent)
        return intent

    def process(self, user_input, context):
        msg = user_input.lower().strip()

        if msg in ["exit", "quit", "stop"]:
            context.set_state("travel_mode", None)
            return "🚪 Exited current mode. What would you like to do next?"

        travel_mode = context.get_state("travel_mode")

        if travel_mode is not None:

            for skill in self.skills:
                if skill.__class__.__name__ == "TravelPlanner":
                    return skill.handle(user_input, context)

        intent = self.detect_intent(user_input)
        context.set("intent", intent)

        for skill in self.skills:
            if skill.__class__.__name__ == intent:
                return skill.handle(user_input, context)

        return self.smart_fallback()

    def smart_fallback(self):
        return (
            "🤖 I couldn't understand that.\n\n"
            "Try:\n"
            "- travel\n"
            "- tech\n"
            "- university\n"
            "- mental health"
        )