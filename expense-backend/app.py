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
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401

    id_token = auth_header.split(' ')[1]

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_email = decoded_token.get('email', 'unknown')
    except Exception as e:
        return jsonify({'error': 'Invalid token'}), 401

    data = request.get_json()
    required_fields = ['date', 'amount', 'category']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Include UID or email if you want per-user tracking
    expense = {
        'user': user_email,
        'uid': uid,
        'date': data['date'],
        'amount': data['amount'],
        'category': data['category'],
        'notes': data.get('notes', ''),
        'timestamp': datetime.utcnow()
    }

    db.collection('expenses').add(expense)
    return jsonify({'message': 'Expense saved successfully'}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)