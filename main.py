from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from linkedin_api_logic import detect_job_change

app = FastAPI()

user_porfiles: Dict[str, Dict[str, str]] = {}

class UserPorfile(BaseModel):
    email: str
    linkedin_url: str

class EmailBody(BaseModel):
    email: str

@app.post("/register")
def register_user(porfile: UserPorfile):
    if porfile.email in user_porfiles:
        raise HTTPException(status_code=400, detail="User already registered")
    user_porfiles[porfile.email] = {"linkedin_url": porfile.linkedin_url}
    return {"message": "User registered successfully"}

@app.post("/porfile")
def create_porfile(porfile: UserPorfile):
    if porfile.email not in user_porfiles:
        raise HTTPException(status_code=404, detail="User not found")
    user_porfiles[porfile.email]["linkedin_url"] = porfile.linkedin_url
    return{"message": "Porfile updated successfully"}

@app.post("/detect_job_changes")
def trigger_job_change_detection(email_body: EmailBody):
    email = email_body.email
    if email not in user_porfiles:
        raise HTTPException(status_code=404, detail="User not found")
    linkedin_url = user_porfiles[email]
    job_change_notification = detect_job_change(linkedin_url)
    return {"message": job_change_notification}

@app.get("/user_porfiles")
def get_user_porfiles():
    return user_porfiles
