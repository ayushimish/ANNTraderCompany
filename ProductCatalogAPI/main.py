from fastapi import FastAPI
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Database connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASS')}"
)

@app.get("/products")
def get_products():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ProductCatalog")  # your table name
    rows = cursor.fetchall()
    return [
        {"id": row[0], "name": row[1], "price": row[2]}
        for row in rows
    ]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ProductCatalog WHERE id = ?", product_id)
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "price": row[2]}
    return {"error": "Product not found"}
