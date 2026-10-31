from flask_restful import Resource

class HelloResource(Resource):
    def get(self):
        from backend_tasks import background_task

        task = background_task.delay()
        return {"message": "hello world!!"}