import firebase_admin
from firebase_admin import credentials, storage, firestore
import uuid

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-service-account.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'your-project-id.appspot.com'
        })

def upload_image_to_storage(file_obj, path: str) -> str:
    bucket = storage.bucket()
    blob = bucket.blob(path)
    blob.upload_from_file(file_obj, content_type="image/png")
    blob.make_public()
    return blob.public_url

def save_metadata_to_firestore(filename: str, url: str):
    db = firestore.client()
    db.collection("images").add({
        "filename": filename,
        "url": url
    })

def fetch_all_images():
    db = firestore.client()
    docs = db.collection("images").stream()
    return [doc.to_dict() for doc in docs]
