from flask import Blueprint, jsonify
from sample_data import CART

cart_bp = Blueprint("cart", __name__)

@cart_bp.get("/")
def get_cart():
    return jsonify(CART)

@cart_bp.post("/add")
def add_to_cart():
    return jsonify({"message": "Item added to cart"})

@cart_bp.post("/remove")
def remove_from_cart():
    return jsonify({"message": "Item removed from cart"})
