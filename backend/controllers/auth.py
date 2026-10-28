from flask_restful import Resource

class LoginResource(Resource):
    def post(self):
        return {"message":"Login route"}

class RegisterResource(Resource):
    def post(self):
        return {"message":"Resource route"}
