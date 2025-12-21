from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)

@admin_bp.get("/dashboard")
def dashboard():
    return jsonify({
        "total_users": 120,
        "total_orders": 45,
        "revenue": 56000
    })
