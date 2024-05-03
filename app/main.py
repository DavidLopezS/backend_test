from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.classes import UserProfile, EmailBody, Database
from app.tools import database_migration as db_import
from app.tools import validators
from fastapi.middleware.cors import CORSMiddleware

db = Database("user_profiles.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_import.create_user_profiles_table(db.db_path)
    yield
    db.cleanup_db_on_exit()

app: FastAPI = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register_user(profile: UserProfile):
    if not validators.validate_email(profile.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if profile.linkedin_url and not validators.validate_url(profile.linkedin_url):
        raise HTTPException(status_code=400, detail="Invalid LinkedIn URL format")

    if profile.job_num < 0:
        raise HTTPException(status_code=400, detail="Invalid job number")
    
    try:
        return db.register_user(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect job changes: {str(e)}")


@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    if not validators.validate_email(email_body.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if email_body.job_num < 0:
        raise HTTPException(status_code=400, detail="Invalid job number")
    
    try:
        return db.detect_job_changes(email_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect job changes: {str(e)}")

@app.get("/user_profiles")
def get_user_profiles():
   try:
        return db.get_user_profiles()
   except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user profiles: {str(e)}")
