import logging
import azure.functions as func
import json

PRODUCTS = [
    {"id": 1, "name": "Apple iPhone 15", "category": "Mobile"},
    {"id": 2, "name": "Samsung Galaxy S24", "category": "Mobile"},
    {"id": 3, "name": "Sony WH-1000XM5", "category": "Headphones"},
    {"id": 4, "name": "MacBook Pro", "category": "Laptop"}
]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing product search request.")

    name = req.params.get('name')
    category = req.params.get('category')
    product_id = req.params.get('id')

    result = PRODUCTS

    if product_id:
        result = [p for p in result if str(p["id"]) == product_id]
    if name:
        result = [p for p in result if name.lower() in p["name"].lower()]
    if category:
        result = [p for p in result if category.lower() in p["category"].lower()]

    return func.HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
