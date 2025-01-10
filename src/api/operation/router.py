from fastapi import APIRouter, HTTPException

from src.api.operation.schemas import OperationHistory
from src.api.operation.services import add_operation_history

router = APIRouter()


@router.post("/add", name="add_operation_history")
async def add_operation_history_endpoint(operation_history_data: OperationHistory):
    try:
        await add_operation_history(operation_history_data)
        return operation_history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
