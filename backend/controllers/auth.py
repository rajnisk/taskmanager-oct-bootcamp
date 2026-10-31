from flask_restful import Resource, request
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, jwt
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

blocklist = set()

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error":"there is no such user with the provided email!"}
        print(password)
        if not check_password_hash(user.password_hash, password):
            return {"error":"incorrect password!"}
        token = create_access_token(identity=str(user.id))

        return {"message":"Loggedin successfully!", "token":token, "role":user.role, "full_name":user.full_name}

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        if not full_name or not email or not password:
            return {"error": "all fields are required!"}
        user = User.query.filter_by(email=email).first()
        if user:
            return {"error": "User already exists!"}
        password_hash = generate_password_hash(password)

        new_user = User(full_name=full_name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return {"message":"User created successfully!"}



# @jwt.token_in_blocklist_loader
# def check_token(jwt_header, jwt_payload):
#     return jwt_payload["jti"] in blocklist

class Logout(Resource):
    @jwt_required()
    def post(self):
        blocklist.add(get_jwt()["jti"])
        return {"message": "Logged out successfully"}, 200