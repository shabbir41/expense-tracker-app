from flask import Flask, request, jsonify
from flask_cors import CORS 
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase Admin SDK
import os, json
cred_json = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app) 

@app.route('/api/expense', methods=['POST'])
def log_expense():
    data = request.get_json()

    # Validate required fields
    required_fields = ['date', 'amount', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Convert to Firestore format
    expense = {
        'date': data['date'],
        'amount': data['amount'],
        'category': data['category'],
        'notes': data.get('notes', ''),
        'timestamp': datetime.utcnow()
    }

    # For now we save under a common collection. Later, per-user.
    db.collection('expenses').add(expense)
    return jsonify({'message': 'Expense saved successfully'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)