import sqlite3
import uuid
from fastapi import FastAPI, HTTPException
from typing import Dict
from app.classes import UserProfile, EmailBody, JobStructure
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

def get_db_connection():
    return sqlite3.connect('user_profiles.db')

def create_user_profiles_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
                          id TEXT PRIMARY KEY,
                          email TEXT,
                          linkedin_url TEXT,
                          current_job_title TEXT,
                          current_job_subtitle TEXT,
                          current_job_caption TEXT,
                          current_job_metadata TEXT
                      )''')
    conn.commit()
    conn.close()

create_user_profiles_table()

@app.post("/register")
def register_user(profile: UserProfile):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        id: str = str(uuid.uuid4())
        current_job: JobStructure = JobStructure.fetch_linkedin_profile(profile.linkedin_url)

        cursor.execute('''INSERT INTO user_profiles (id, email, linkedin_url, current_job_title, current_job_subtitle, current_job_caption, current_job_metadata)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                          (id, profile.linkedin_url, current_job.title, current_job.subtitle, current_job.caption, current_job.metadata))
        
        conn.commit()
        conn.close()

        return {"message": "User registered profile successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 

@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    try: 
        conn = get_db_connection()
        cursor = conn.cursor()

        email: str = email_body.email

        cursor.execute('SELECT * FROM user_profiles WHERE email=?', (email))
        user_profile = cursor.fetchone()
        if not  user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        linkedin_url: str = user_profile[2]
        user_new_job: JobStructure = JobStructure.fetch_linkedin_profile(linkedin_url)

        if user_profile[3:7] == (user_new_job.title, user_new_job.subtitle, user_new_job.caption, user_new_job.metadata):
            conn.close()

            return {
                "message": "No job change detected",
                "User_job": {
                    "title": user_profile[3],
                    "subtitle": user_profile[4],
                    "caption": user_profile[5],
                    "metadata": user_profile[6]
                }
            }
        else:
            cursor.execute('''UPDATE user_profiles
                            SET current_job_title=?, current_job_subtitle=?, current_job_caption=?, current_job_metadata=?
                            WHERE email=?''',
                            (user_new_job.title, user_new_job.subtitle, user_new_job.caption, user_new_job.metadata, email))
            conn.commit()
            conn.close()

            return {
                "message": "Job change detected",
                "User_job": {
                    "title": user_new_job.title,
                    "subtitle": user_new_job.subtitle,
                    "caption": user_new_job.caption,
                    "metadata": user_new_job.metadata
                }
            }
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 


@app.get("/user_profiles")
def get_user_profiles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_profiles')
        user_profiles = cursor.fetchall()
        conn.close()

        if user_profiles:
            return user_profiles
        else:
            raise HTTPException(status_code=404, detail="No users registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

