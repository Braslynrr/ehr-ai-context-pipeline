
from ehr_ai_core.redis.redis import RedisManager
from services.tools.Itool import ITool


class ehr_redis_save(ITool):
    redis:RedisManager

    def __init__(self, redis: RedisManager):
        super().__init__()
        self.redis = redis
        self.name = "ehr_redis_save"
        self.description = "save pending action in redis"

    def run(self, input):
        id = self.redis.save_data(input["json_data"], input["doctor"])
        input["pending_action_id"] = id
        return {"pending_action_id" : id}