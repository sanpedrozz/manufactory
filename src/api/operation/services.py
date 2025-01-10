from datetime import datetime

from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import OperationHistory as OperationHistoryDB
from src.api.operation.schemas import OperationHistory as OperationHistorySchema


async def add_operation_history(operation_history_data: OperationHistorySchema):
    async with AsyncSessionFactory() as session:
        async with session.begin():
            new_operation = OperationHistoryDB(
                place_id=operation_history_data.place,
                program=operation_history_data.program,
                text=operation_history_data.data if operation_history_data.data else "",
                dt_created=datetime.now(),
            )
            await new_operation.add(session)
