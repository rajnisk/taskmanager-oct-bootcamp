from controllers.auth import LoginResource, RegisterResource
from controllers.hello import HelloResource

def register_routes(api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(HelloResource, '/')