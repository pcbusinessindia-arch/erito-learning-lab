from flask import Flask, jsonify
from flask_cors import CORS
from database import get_connection

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


if __name__ == "__main__":
    app.run(debug=True)