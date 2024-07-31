from fastapi import APIRouter
from pydantic import BaseModel, Extra
from src.utils.chat import OpenaiChatProvider

router = APIRouter()


class PostBody(BaseModel, extra=Extra.allow):
    drugs: list[str]
    user: str


@router.post("")
async def post(body: PostBody) -> str:
    chat_provider = OpenaiChatProvider()
    for drug in body.drugs:
        chat_provider.add_message(drug)
    return chat_provider.add_message(body.user)
