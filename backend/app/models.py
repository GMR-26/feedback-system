from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    team_id = Column(Integer)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    strengths = Column(Text)
    improvements = Column(Text)
    sentiment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Integer, default=0)
