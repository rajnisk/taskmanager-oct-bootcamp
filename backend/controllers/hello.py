from backend_tasks import background_task
from flask_restful import Resource

class HelloResource(Resource):
    def get(self):
        task = background_task.delay()
        return {"message": "hello world!!"}