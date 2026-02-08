import firebase_admin
from firebase_admin import credentials, db, firestore
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
# On Railway, we'll use an environment variable 'FIREBASE_SERVICE_ACCOUNT' holding the JSON string
service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
database_url = os.getenv("FIREBASE_DATABASE_URL", "https://music-app-f2e65-default-rtdb.asia-southeast1.firebasedatabase.app")

if not firebase_admin._apps:
    try:
        if service_account_json:
            # Load from environment variable (JSON string)
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print("Firebase Admin Initialized from environment variable")
        else:
            # Fallback to local file for development
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': database_url
                })
                print(f"Firebase Admin Initialized with {cred_path}")
            else:
                print("Warning: No Firebase credentials found (env or file).")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

def get_db_ref(path: str):
    return db.reference(path)

def get_firestore_client():
    return firestore.client()
