from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get() -> str:
    return "Success"
