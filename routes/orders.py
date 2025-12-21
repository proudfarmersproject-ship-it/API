from flask import Blueprint, jsonify
from sample_data import ORDERS

orders_bp = Blueprint("orders", __name__)

@orders_bp.post("/")
def place_order():
    return jsonify({
        "order_id": "o2",
        "status": "pending"
    })

@orders_bp.get("/")
def list_orders():
    return jsonify(ORDERS)
