from fastapi import FastAPI, HTTPException
from typing import Dict
from app.classes import UserProfile, EmailBody, JobStructure
import sqlite3

app = FastAPI()

user_profiles: Dict[str, Dict[str, JobStructure]] = {}
#TODO Make that on register the user saves it's current job position. And make that detect_job_changes a cronjob that keeps checking if the user has a new job
@app.post("/register")
def register_user(profile: UserProfile):
    try:
        if profile.email in user_profiles:
            raise HTTPException(status_code=400, detail="User already has a registered profile")
        
        user_profiles[profile.email] = {"linkedin_url": profile.linkedin_url, "current_job": JobStructure.fetch_linkedin_profile(profile.linkedin_url)}
        return {"message": "User registered profile successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 

@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    try: 
        email = email_body.email
        if email not in user_profiles:
            raise HTTPException(status_code=404, detail="User not found")
        
        linkedin_url = user_profiles[email]
        user_new_job = JobStructure.fetch_linkedin_profile(linkedin_url)

        if "current_job" in user_profiles[email] and user_profiles[email]["current_job"].equals(user_new_job):
            return {
                "message": "No job change detected",
                "User_job": user_profiles[email]["current_job"]
            }
        else:
            user_profiles[email]["current_job"] = user_new_job
            return {
                "message": "Job change detected",
                "User_job": user_profiles[email]["current_job"]
            }
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 


@app.get("/user_profiles")
def get_user_profiles():
    if user_profiles:
        return user_profiles
    else:
        raise HTTPException(status_code=404, detail="No users registered")
