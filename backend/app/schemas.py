from pydantic import BaseModel
from datetime import datetime

class UserLogin(BaseModel):
    name: str

class FeedbackCreate(BaseModel):
    employee_id: int
    manager_id: int
    strengths: str
    improvements: str
    sentiment: str

class FeedbackOut(BaseModel):
    id: int
    employee_id: int
    manager_id: int
    strengths: str
    improvements: str
    sentiment: str
    timestamp: datetime
    acknowledged: int

    class Config:
        orm_mode = True
