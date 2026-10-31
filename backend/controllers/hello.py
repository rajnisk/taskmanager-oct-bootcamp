from flask_restful import Resource
from extensions import cache
from datetime import datetime


class HelloResource(Resource):
    def get(self):
        from backend_tasks import background_task
        task = background_task.delay()
        return {"message": "hello world!!"}

class CacheTestResource(Resource):
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        print("GET request received")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"message": "this is get method!", "time": time_now}, 200
