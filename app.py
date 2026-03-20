from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT role FROM users WHERE username=? AND password=?", (username,password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"status":"success", "role": user[0]}
    else:
        return {"status":"fail"}

# Add contract (buyers only)
@app.route('/add_contract', methods=['POST'])
def add_contract():
    data = request.json
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO contracts (crop, price, quantity, buyer) VALUES (?, ?, ?, ?)",
                 (data['crop'], data['price'], data['quantity'], data['buyer']))
    conn.commit()
    conn.close()
    return {"message": "Contract added"}

# Get all contracts
@app.route('/contracts', methods=['GET'])
def get_contracts():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM contracts")
    contracts = []
    for row in cursor:
        contracts.append({
            "id": row[0],
            "crop": row[1],
            "price": row[2],
            "quantity": row[3],
            "buyer": row[4]
        })
    conn.close()
    return jsonify(contracts)

# Accept contract (farmers only)
@app.route('/accept_contract/<int:contract_id>', methods=['POST'])
def accept_contract(contract_id):
    conn = sqlite3.connect('database.db')
    conn.execute("UPDATE contracts SET buyer = buyer || ' (Accepted)' WHERE id = ?", (contract_id,))
    conn.commit()
    conn.close()
    return {"message": "Contract accepted!"}

app.run(debug=True)