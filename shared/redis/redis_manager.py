import json

import redis


class RedisManager:
    def __init__(self, host='redis', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def add_to_queue(self, queue_name: str, data: dict):
        """Добавить данные в очередь."""
        serialized_data = json.dumps(data)
        self.client.rpush(queue_name, serialized_data)

    def get_from_queue(self, queue_name: str):
        """Получить данные из очереди."""
        data = self.client.lpop(queue_name)
        if data:
            return json.loads(data)
        return None

    def get_all_from_queue(self, queue_name: str) -> list:
        """Получить все данные из очереди."""
        data = self.client.lrange(queue_name, 0, -1)
        self.client.ltrim(queue_name, len(data), -1)  # Удаляем все элементы после извлечения
        return [json.loads(item) for item in data]

    def get_queue_length(self, queue_name: str) -> int:
        """Получить длину очереди."""
        return self.client.llen(queue_name)

    def get_all_keys(self) -> list:
        """Получить список всех ключей в Redis."""
        return self.client.keys("*")
