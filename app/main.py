from fastapi import FastAPI, HTTPException
from typing import Dict
from app.linkedin_api_logic import fetch_linkedin_profile
from app.classes import UserProfile, EmailBody

app = FastAPI()

user_profiles: Dict[str, Dict[str, str]] = {}

@app.post("/register")
def register_user(profile: UserProfile):
    try:
        if profile.email in user_profiles:
            raise HTTPException(status_code=400, detail="User already registered")
        
        user_profiles[profile.email] = {"linkedin_url": profile.linkedin_url}
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 

@app.post("/profile")
def create_profile(profile: UserProfile):
    try:
        if profile.email not in user_profiles:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_profiles[profile.email]["linkedin_url"] = profile.linkedin_url
        return{"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 


@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    try: 
        email = email_body.email
        if email not in user_profiles:
            raise HTTPException(status_code=404, detail="User not found")
        
        linkedin_url = user_profiles[email]
        job_change_notification = fetch_linkedin_profile(linkedin_url)
        if job_change_notification is Exception:
            raise HTTPException(status_code=500, detail=f"An error occured: {job_change_notification}")
         
        return {"message": job_change_notification}
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"An error occured: {e}") 


@app.get("/user_profiles")
def get_user_profiles():
    if user_profiles:
        return user_profiles
    else:
        raise HTTPException(status_code=404, detail="No users registered")
