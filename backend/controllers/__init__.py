from controllers.auth import LoginResource, RegisterResource, Logout
from controllers.hello import HelloResource
from controllers.task import EmployeeResource, TaskResource

def register_routes(api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(HelloResource, '/')
    api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')
    api.add_resource(EmployeeResource, '/employees')
    api.add_resource(Logout, '/logout')