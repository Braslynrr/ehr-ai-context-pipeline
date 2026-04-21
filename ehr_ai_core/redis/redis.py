import os
from redis import Redis, exceptions
import uuid
import json

from ehr_ai_core.error.app_error import AppError


class RedisManager:

    def __init__(self):
        self.__host = os.getenv("REDIS_HOST", "ehr_redis")
        self.__port = os.getenv("REDIS_PORT", 6379)

        self.__client = Redis(
            host=self.__host,
            port=self.__port,
            decode_responses=True
        )

    def save_data(self, data: dict, prefix:str|None = None):
        try:
            stream_id = str(uuid.uuid4())
            if prefix:
                stream_id += f"{prefix}:{stream_id}"
                
            self.__client.setex(
                stream_id,
                300,
                json.dumps(data)
            )

            return stream_id

        except exceptions.RedisError as e:
    
            raise AppError("Redis save failed", 500)

    def get_by_id(self, id: str):
        try:
            data = self.__client.get(id)

            if not data:
                raise AppError("Stream not found or expired", 404)
            
            self.__client.delete(id)

            return json.loads(data)

        except exceptions.RedisError:
            raise AppError("Redis read failed", 500)