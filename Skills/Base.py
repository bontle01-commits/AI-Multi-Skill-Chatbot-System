from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL


DATABASE_URL = "postgresql+psycopg2://postgres:%40Retshepile12@localhost:5432/chatbot_project"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Skill:
    """
    Base class for all chatbot skills.
    Every skill (FAQ, Travel, TechSupport, MentalHealth)
    must inherit from this class.
    """

    def can_handle(self, user_input, context):
        """
        Return True if this skill should handle the input.
        Must be overridden in child classes.
        """
        raise NotImplementedError("can_handle() must be implemented")

    def handle(self, user_input, context):
        """
        Generate response for the user input.
        Must be overridden in child classes.
        """
        raise NotImplementedError("handle() must be implemented")


def init_db():
    """
    Initialize the database by creating all tables
    defined in ORM models that inherit from Base.
    """
    Base.metadata.create_all(bind=engine)
