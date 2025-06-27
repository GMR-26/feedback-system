from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, routes, database
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routes.router)

models.Base.metadata.create_all(bind=database.engine)

def seed_users():
    db: Session = database.SessionLocal()
    if db.query(models.User).count() == 0:
        db.add_all([
            models.User(name="Alice", role="manager", team_id=1),
            models.User(name="Bob", role="employee", team_id=1),
            models.User(name="Charlie", role="employee", team_id=1)
        ])
        db.commit()
    db.close()

seed_users()
