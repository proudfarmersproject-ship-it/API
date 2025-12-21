USERS = [
    {
        "id": "u1",
        "email": "john@example.com",
        "role": "customer",
        "token": "mock-jwt-token",
        "fullname": "John Doe"
    }
]

CATEGORIES = [
    {"id": "c1", "name": "Electronics"},
    {"id": "c2", "name": "Fashion"}
]

PRODUCTS = [
    {
        "id": "p1",
        "name": "iPhone 15",
        "description": "Latest Apple phone",
        "category_id": "c1",
        "price": 1200,
        "images": [
            {"url": "/img/iphone.png", "is_primary": True}
        ]
    }
]

CART = {
    "items": [
        {
            "product_id": "p1",
            "variant_id": "v1",
            "name": "iPhone 15 - 128GB",
            "price": 1200,
            "quantity": 1
        }
    ],
    "total": 1200
}

ORDERS = [
    {
        "id": "o1",
        "status": "confirmed",
        "total": 1200,
        "created_at": "2025-01-01"
    }
]
