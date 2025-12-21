from flask import Blueprint, jsonify
from sample_data import CATEGORIES

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("/")
def list_categories():
    return jsonify(CATEGORIES)
