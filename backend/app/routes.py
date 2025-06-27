from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": db_user.id,
        "name": db_user.name,
        "role": db_user.role,
        "team_id": db_user.team_id
    }

@router.get("/users/team/{team_id}")
def get_team_members(team_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.team_id == team_id, models.User.role == "employee").all()

@router.post("/feedback")
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/feedback/employee/{employee_id}", response_model=list[schemas.FeedbackOut])
def get_feedback_for_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(models.Feedback).filter(models.Feedback.employee_id == employee_id).all()

@router.patch("/feedback/{feedback_id}/acknowledge")
def acknowledge(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.acknowledged = 1
    db.commit()
    return {"message": "Acknowledged"}

@router.get("/feedback/manager/{manager_id}/sentiment-stats")
def get_sentiment_stats(manager_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import func
    result = db.query(models.Feedback.sentiment, func.count(models.Feedback.id))\
        .filter(models.Feedback.manager_id == manager_id)\
        .group_by(models.Feedback.sentiment).all()
    return {s: c for s, c in result}
