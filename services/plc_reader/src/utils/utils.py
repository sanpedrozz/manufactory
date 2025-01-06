import json
from hashlib import md5

from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import Place, PlaceStatus


async def get_places_by_status(status: PlaceStatus):
    """
    Фильтрует записи Place по заданному статусу.
    :param status: Строка со статусом, по которому нужно фильтровать.
    :return: Список объектов Place, соответствующих условиям.
    """
    async with AsyncSessionFactory() as session:
        return await Place.get_all(session, Place.status == status)


def compute_hash(value):
    return md5(json.dumps(value, sort_keys=True).encode()).hexdigest()
