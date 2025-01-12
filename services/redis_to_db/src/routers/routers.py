from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def check():
    """
    Проверка состояния приложения.
    """
    return {"status": "ok"}
