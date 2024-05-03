from fastapi import FastAPI
from app.classes import UserProfile, EmailBody, Database
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "user_profiles.db"

db = Database(DB_PATH)
db.create_user_profiles_table()

@app.post("/register")
def register_user(profile: UserProfile):
    return db.register_user(profile)

@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    return db.detect_job_changes(email_body)

@app.get("/user_profiles")
def get_user_profiles():
   return db.get_user_profiles()
