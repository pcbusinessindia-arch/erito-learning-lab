from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import get_connection
import mysql.connector
import os

app = Flask(__name__)

CORS(app)


# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Home page
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# Serve lesson pages
@app.route("/lessons/<path:filename>")
def lessons(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "lessons"),
        filename
    )


# Serve CSS files
@app.route("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "css"),
        filename
    )


# Serve JavaScript files
@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "js"),
        filename
    )


# Get customers
@app.route("/api/customers")
def customers():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM customers")

        rows = cursor.fetchall()

        customers_data = []

        for row in rows:

            customers_data.append({
                "id": row[0],
                "name": row[1],
                "city": row[2]
            })

        return jsonify(customers_data)

    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# Execute student's SQL query
@app.route("/api/query", methods=["POST"])
def execute_query():

    data = request.get_json()

    query = data.get("query", "").strip()


    # Only allow SELECT queries
    if not query.lower().startswith("select"):

        return jsonify({
            "error": "Only SELECT queries are allowed."
        }), 400


    connection = None
    cursor = None


    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]


        return jsonify({
            "columns": columns,
            "rows": rows
        })


    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 400


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)