from flask import Blueprint, jsonify

coupons_bp = Blueprint("coupons", __name__)

@coupons_bp.post("/apply")
def apply_coupon():
    return jsonify({
        "code": "NEW10",
        "discount": 100
    })
