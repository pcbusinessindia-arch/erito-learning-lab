from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection
import mysql.connector

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "Erito Learning Lab API is running!"


@app.route("/api/customers")
def customers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    customers_data = []

    for row in rows:
        customers_data.append({
            "id": row[0],
            "name": row[1],
            "city": row[2]
        })

    return jsonify(customers_data)


@app.route("/api/query", methods=["POST"])
def execute_query():

    data = request.get_json()
    query = data.get("query", "").strip()

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

        columns = [column[0] for column in cursor.description]

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


if __name__ == "__main__":
    app.run(debug=True)