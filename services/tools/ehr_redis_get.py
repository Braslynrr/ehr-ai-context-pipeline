from ehr_ai_core.redis.redis import RedisManager
from services.tools.Itool import ITool


class ehr_redis_get(ITool):
    redis:RedisManager

    def __init__(self, redis: RedisManager):
        super().__init__()
        self.redis = redis
        self.name = "ehr_redis_get"
        self.description = "get pending action in redis"

    def run(self, input):
        data = self.redis.get_by_id(input["pending_action_id"])
        input["json_data"] = data
        return data