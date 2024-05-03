import sqlite3
import uuid
import requests
import os
from pydantic import BaseModel
from typing import Dict, List, Optional
from fastapi import HTTPException


class UserProfile(BaseModel):
    email: str
    linkedin_url: str
    job_num: int

class EmailBody(BaseModel):
    email: str
    job_num: int

class JobStructure(BaseModel):
    title: str
    subtitle: Optional[str]
    caption: Optional[str]
    metadata: Optional[str]

    @classmethod
    def fetch_linkedin_profile(cls, linkedin_url: str, job_num: int):
        try:
            rapid_api_key: str = os.environ['X_RAPID_API_KEY']
            rapid_api_host: str = os.environ['X_RAPID_API_HOST']
            api_endpoint: str = os.environ['URL']

            headers: Dict[str, str] = {
                "content-type": "application/json",
                "X-RapidAPI-Key": rapid_api_key,
                "X-RapidAPI-Host": rapid_api_host
            }
            payload: Dict[str, str] = {"link": linkedin_url}
            
            response = requests.post(api_endpoint, json=payload, headers=headers)
            response.raise_for_status()
        
            experiences = response.json().get('data', {}).get('experiences', [])
            if experiences:
                job_data = experiences[job_num]
                return cls(title=job_data.get('title'), subtitle=job_data.get('subtitle'), caption=job_data.get('caption'), metadata=job_data.get('metadata'))
            else:
                return cls(title='No job found')
        except requests.exceptions.RequestException as e:
            return cls(title=f"Request error: {e}")
        except Exception as e:
            return cls(title=f"Error: {e}") 
    
    def equals(self, other: 'JobStructure') -> bool:
        return(
            self.title == other.title and
            self.subtitle == other.subtitle and
            self.caption == other.caption and
            self.metadata == other.metadata
        )

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_user_profiles_table(self):
        try:
            conn = self.get_connection()
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
        except Exception as e:
            print(f"Error while creating the db: {e}")
    
    def cleanup_db_on_exit(self):
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print("Database deleted on exit")
            else:
                print("Database file not found") 
        except Exception as e:
            print(f"Error in cleanup_db_on_exit: {e}") 
    
    def register_user(self, profile: UserProfile):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            user_id = str(uuid.uuid4())
            current_job = JobStructure.fetch_linkedin_profile(profile.linkedin_url, profile.job_num)

            cursor.execute('''INSERT INTO user_profiles (id, email, linkedin_url, current_job_title, current_job_subtitle, current_job_caption, current_job_metadata)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                              (user_id, profile.email, profile.linkedin_url, current_job.title, current_job.subtitle, current_job.caption, current_job.metadata))
            
            conn.commit()
            conn.close()

            return {"message": "User registered profile successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occured: {e}")
    
    def detect_job_changes(self, email_body: EmailBody):
        try: 
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM user_profiles WHERE email=?', (email_body.email,))
            user_profile = cursor.fetchone()
            if not user_profile:
                raise HTTPException(status_code=404, detail="User not found")
            
            linkedin_url = user_profile[2]
            user_new_job = JobStructure.fetch_linkedin_profile(linkedin_url, email_body.job_num)

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
                                (user_new_job.title, user_new_job.subtitle, user_new_job.caption, user_new_job.metadata, email_body.email))
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
    
    def get_user_profiles(self) ->List[Dict]:
        try:
            conn = self.get_connection()
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
    

