import json
from hashlib import md5

from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import Place


async def get_places_with_name_containing(keyword: str):
    """
    Фильтрует записи Place, которые содержат определенный keyword в названии.
    :param keyword: Строка с частью названия.
    :return: Список объектов Place, соответствующих условиям.
    """
    async with AsyncSessionFactory() as session:
        return await Place.get_all(session, Place.name.like(f"%{keyword}%"))


def compute_hash(value):
    return md5(json.dumps(value, sort_keys=True).encode()).hexdigest()
