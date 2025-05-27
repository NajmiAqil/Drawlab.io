from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, storage
import uuid

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-service-account.json")  # Pastikan file ini tersedia
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com'
})
bucket = storage.bucket()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    blob = bucket.blob(f"images/{uuid.uuid4()}.png")
    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()
    return {"url": blob.public_url}
