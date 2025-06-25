from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Feedback System Backend Running"}
