from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models.user import User
from extensions import db

user_fields = {
    'id': fields.Integer,
    'First_name': fields.String,
    'Last_name': fields.String,
    'email': fields.String,
    'phone': fields.Integer,
    'role': fields.String,
    'created_at': fields.DateTime
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('id', type=int, required=True)
user_parser.add_argument('First_name', type=str, required=True)
user_parser.add_argument('Last_name', type=str, required=True)
user_parser.add_argument('email', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)
user_parser.add_argument('phone', type=int)
user_parser.add_argument('role', type=str, choices=['customer', 'admin'])

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('First_name', type=str)
user_update_parser.add_argument('Last_name', type=str)
user_update_parser.add_argument('email', type=str)
user_update_parser.add_argument('phone', type=int)
user_update_parser.add_argument('role', type=str)

class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(
            id=args['id'],
            First_name=args['First_name'],
            Last_name=args['Last_name'],
            email=args['email'],
            phone=args.get('phone'),
            role=args.get('role', 'customer')
        )
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get_or_404(id)
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_update_parser.parse_args()
        user = User.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user
    
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 204

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if not user or not user.check_password(args['password']):
            abort(401, message='Invalid credentials')
        return {
            'message': 'Login successful',
            'user_id': user.id,
            'role': user.role
        }, 200
