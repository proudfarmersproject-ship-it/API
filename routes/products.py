from flask import Blueprint, jsonify
from sample_data import PRODUCTS

products_bp = Blueprint("products", __name__)

@products_bp.get("/")
def list_products():
    return jsonify(PRODUCTS)

@products_bp.get("/<product_id>")
def product_detail(product_id):
    return jsonify(PRODUCTS[0])
