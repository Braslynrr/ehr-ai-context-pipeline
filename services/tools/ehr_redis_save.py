
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
        data = dict(input)
        
        data.pop("ehr_json")
        
        id = self.redis.save_action(data, input["doctor"])
        input["pending_action_id"] = id
        return {"pending_action_id" : id}