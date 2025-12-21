from flask import Blueprint, jsonify

addresses_bp = Blueprint("addresses", __name__)

@addresses_bp.get("/")
def list_addresses():
    return jsonify([
        {
            "id": "a1",
            "city": "Bangalore",
            "pincode": "560001",
            "is_default": True
        }
    ])

@addresses_bp.post("/")
def add_address():
    return jsonify({"message": "Address added"})
