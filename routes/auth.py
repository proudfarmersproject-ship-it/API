from flask import Blueprint, jsonify, request
from sample_data import USERS

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    return jsonify(USERS[0])

@auth_bp.post("/register")
def register():
    return jsonify({"message": "User registered"}), 201

@auth_bp.get("/me")
def me():
    return jsonify(USERS[0])
