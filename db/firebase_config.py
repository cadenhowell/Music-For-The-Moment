import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

db_url = "https://music-for-the-moment-61327-default-rtdb.firebaseio.com"


if not firebase_admin._apps:
    cred = credentials.Certificate("./db/firebase_key.json")
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})

ref = db.reference('/')


