from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)  # "manager" or "employee"
    team_id = Column(Integer)  # optional for manager-employee mapping

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    strengths = Column(Text)
    improvements = Column(Text)
    sentiment = Column(String)  # "positive" / "neutral" / "negative"
    timestamp = Column(String)
    acknowledged = Column(Integer, default=0)
