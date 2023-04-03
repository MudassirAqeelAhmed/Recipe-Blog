from flask_restx import Resource, Namespace, fields
from models import Recipe, User
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token


auth_ns = Namespace("auth", description="A namespace for authentication")

signup_model = auth_ns.model(
        'Signup', {
            'username': fields.String(),
            'email': fields.String(),
            'password': fields.String(),
        }
)

login_model = auth_ns.model(
        'Login', {
            'username': fields.String(),
            'password': fields.String(),
        }
)

@auth_ns.route('/signup')
class Signup(Resource):
    
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data['username']
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message": f"User with the username {username} already exists"})

        new_user = User(username=data['username'], 
                        email=data['email'],
                        password=generate_password_hash(data['password']))
        new_user.save()
        return jsonify({"message": "User created successfully"})
    
@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password,password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return jsonify({"access_token": access_token,
                            "refresh_token": refresh_token})
