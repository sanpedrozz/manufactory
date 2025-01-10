import redis

# Подключение к Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Проверка подключения
try:
    redis_client.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Failed to connect to Redis")

# Получение всех ключей
keys = redis_client.keys('*')
print(f"Keys in Redis: {keys}")

# Получение значения по ключу
for key in keys:
    key_type = redis_client.type(key)
    if key_type == "string":
        value = redis_client.get(key)
        print(f"Key: {key}, Value: {value}")
    elif key_type == "list":
        value = redis_client.lrange(key, 0, -1)  # Получить весь список
        print(f"Key: {key}, List: {value}")
    elif key_type == "hash":
        value = redis_client.hgetall(key)  # Получить все поля и значения
        print(f"Key: {key}, Hash: {value}")
    elif key_type == "set":
        value = redis_client.smembers(key)  # Получить все элементы множества
        print(f"Key: {key}, Set: {value}")
    elif key_type == "zset":
        value = redis_client.zrange(key, 0, -1, withscores=True)  # Получить отсортированные элементы с их весами
        print(f"Key: {key}, Sorted Set: {value}")
    else:
        print(f"Key: {key} has an unknown type: {key_type}")
