import logging
import pyodbc
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing product search request.')

    query = req.params.get('query')
    if not query:
        return func.HttpResponse(
            "Please provide a 'query' parameter in the URL.",
            status_code=400
        )

    try:
        # Connection string from local.settings.json / Application Settings
        conn_str = os.environ["SQL_CONNECTION_STRING"]

        # Connect to Azure SQL Database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Perform the search
        sql_query = """
            SELECT ProductID, ProductName, Price, Stock, CategoryID, ImageURL
            FROM ProductCatalog
            WHERE LOWER(ProductName) LIKE LOWER(?)
        """
        cursor.execute(sql_query, ('%' + query + '%',))
        rows = cursor.fetchall()

        if not rows:
            return func.HttpResponse("No products found matching the query.", status_code=404)

        # Build response
        results = []
        for row in rows:
            results.append({
                "ProductID": row.ProductID,
                "ProductName": row.ProductName,
                "Price": row.Price,
                "Stock": row.Stock,
                "CategoryID": row.CategoryID,
                "ImageURL": row.ImageURL
            })

        return func.HttpResponse(str(results), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )
