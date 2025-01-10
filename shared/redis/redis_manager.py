import json

import redis


class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def add_to_queue(self, queue_name: str, data: dict):
        """Добавить данные в очередь."""
        serialized_data = json.dumps(data)
        self.client.rpush(queue_name, serialized_data)

    def get_from_queue(self, queue_name: str):
        """Получить данные из очереди."""
        serialized_data = self.client.lpop(queue_name)
        if serialized_data:
            return json.loads(serialized_data)
        return None

    def get_queue_length(self, queue_name: str) -> int:
        """Получить длину очереди."""
        return self.client.llen(queue_name)
