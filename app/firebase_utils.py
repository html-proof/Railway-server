import firebase_admin
from firebase_admin import credentials, db, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
# Ensure you have the serviceAccountKey.json in the backend root or set FIREBASE_CREDENTIALS_PATH
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
database_url = os.getenv("FIREBASE_DATABASE_URL", "https://music-app-f2e65-default-rtdb.asia-southeast1.firebasedatabase.app")

if not firebase_admin._apps:
    try:
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print(f"Firebase Admin Initialized with {cred_path}")
        else:
            print(f"Warning: Firebase credentials not found at {cred_path}. Firebase features may fail.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

def get_db_ref(path: str):
    return db.reference(path)

def get_firestore_client():
    return firestore.client()
