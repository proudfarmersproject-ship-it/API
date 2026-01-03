from flask_restful import Resource, reqparse, fields, marshal_with
from models.address import Address
from extensions import db

address_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'full_name': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'address_line1': fields.String,
    'city': fields.String,
    'pincode': fields.String,
    'is_default': fields.Integer
}

address_parser = reqparse.RequestParser()
address_parser.add_argument('user_id', type=int, required=True)
address_parser.add_argument('full_name', type=str, required=True)
address_parser.add_argument('phone', type=str, required=True)
address_parser.add_argument('email', type=str, required=True)
address_parser.add_argument('address_line1', type=str, required=True)
address_parser.add_argument('city', type=str, required=True)
address_parser.add_argument('pincode', type=str, required=True)
address_parser.add_argument('is_default', type=int, choices=[0, 1])

class AddressListResource(Resource):
    @marshal_with(address_fields)
    def get(self):
        addresses = Address.query.all()
        return addresses
    
    @marshal_with(address_fields)
    def post(self):
        args = address_parser.parse_args()
        address = Address(**args)
        db.session.add(address)
        db.session.commit()
        return address, 201

class AddressResource(Resource):
    @marshal_with(address_fields)
    def get(self, id):
        address = Address.query.get_or_404(id)
        return address
    
    @marshal_with(address_fields)
    def patch(self, id):
        args = address_parser.parse_args()
        address = Address.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(address, key, value)
        db.session.commit()
        return address
    
    def delete(self, id):
        address = Address.query.get_or_404(id)
        db.session.delete(address)
        db.session.commit()
        return {'message': 'Address deleted'}, 204