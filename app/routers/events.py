from fastapi import APIRouter


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/")
async def get_events():
    return {"message": "List of events"}
