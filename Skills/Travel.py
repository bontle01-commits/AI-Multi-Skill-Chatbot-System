from Skills.Base import Skill, SessionLocal
from sqlalchemy import Column, Integer, String
from Skills.Base import Base


class TravelEntry(Base):
    __tablename__ = "travel"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    response = Column(String, nullable=False)


class TravelPlanner(Skill):

    def handle(self, user_input, context):
        msg = user_input.lower().strip()
        db = SessionLocal()

        try:
            travel_mode = context.get_state("travel_mode")

            if travel_mode is None:
                context.set_state("travel_mode", "menu")
                return (
                    "🌍 Travel Assistant Activated\n\n"
                    "Choose an option:\n"
                    "1. ✈️ Flight Booking\n"
                    "2. 🏨 Hotel Booking\n"
                    "3. 🗺️ Full Trip Planning\n"
                    "4. 🌏 Popular Destinations\n"
                    "5. 🚪 Exit Travel Mode\n\n"
                    "Reply with a number (1–5)."
                )

            if travel_mode == "menu":

                if msg == "1":
                    context.set_state("travel_mode", "Flight Booking")
                    context.set_state("travel_Flight Booking", [])
                    return "✈️ Enter departure city"

                if msg == "2":
                    context.set_state("travel_mode", "Hotel Booking")
                    context.set_state("travel_Hotel Booking", [])
                    return "🏨 Enter city"

                if msg == "3":
                    context.set_state("travel_mode", "Full Trip Planning")
                    return "🗺️ Tell me destination, budget, and dates"

                if msg == "4":
                    return "🌏 Try: Paris, Dubai, Cape Town, Bali"

                if msg == "5":
                    context.set_state("travel_mode", None)
                    return "🚪 Travel mode closed"

                return "❗ Please reply with 1–5"

            if travel_mode == "Flight Booking":
                session_key = "travel_Flight Booking"
                history = context.get_state(session_key) or []
                history.append(user_input)
                context.set_state(session_key, history)

                if len(history) == 1:
                    return "✈️ Now tell me destination"

                elif len(history) == 2:
                    return "📅 Now tell me travel date"

                else:
                    departure, destination, date = history

                    context.set_state("travel_mode", "menu")
                    context.set_state(session_key, [])

                    return (
                        f"✈️ Flight booked!\n\n"
                        f"From: {departure.title()}\n"
                        f"To: {destination.title()}\n"
                        f"Date: {date}\n\n"
                        "🔙 Back to Travel Menu:\n"
                        "1. ✈️ Flight Booking\n"
                        "2. 🏨 Hotel Booking\n"
                        "3. 🗺️ Full Trip Planning\n"
                        "4. 🌏 Popular Destinations\n"
                        "5. 🚪 Exit Travel Mode"
                    )

            if travel_mode == "Hotel Booking":
                session_key = "travel_Hotel Booking"
                history = context.get_state(session_key) or []
                history.append(user_input)
                context.set_state(session_key, history)

                if len(history) == 1:
                    return "🏨 Now tell me check-in date"

                elif len(history) == 2:
                    return "🏨 Now tell me check-out date"

                else:
                    city, checkin, checkout = history

                    context.set_state("travel_mode", "menu")
                    context.set_state(session_key, [])

                    return (
                        f"🏨 Hotel booked in {city.title()}!\n\n"
                        f"Check-in: {checkin}\n"
                        f"Check-out: {checkout}\n\n"
                        "🔙 Back to Travel Menu:\n"
                        "1. ✈️ Flight Booking\n"
                        "2. 🏨 Hotel Booking\n"
                        "3. 🗺️ Full Trip Planning\n"
                        "4. 🌏 Popular Destinations\n"
                        "5. 🚪 Exit Travel Mode"
                    )

            if travel_mode == "Full Trip Planning":
                return "🗺️ Tell me destination, budget, and dates"

            return "Say 'travel' to start 🌍"

        finally:
            db.close()