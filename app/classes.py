import requests
import os
from pydantic import BaseModel
from typing import Dict


class UserProfile(BaseModel):
    email: str
    linkedin_url: str

class EmailBody(BaseModel):
    email: str

class JobStructure(BaseModel):
    title: str
    subtitle: str
    caption: str
    metadata: str

    @classmethod
    def fetch_linkedin_profile(cls, linkedin_url: str):
        rapid_api_key: str = os.environ.get('X_RAPID_API_KEY', '')
        rapid_api_host: str = os.environ.get('X_RAPID_API_HOST', '')
        api_endpoint: str = os.environ.get('URL', '')

        headers: Dict[str, str] = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{rapid_api_key}",
            "X-RapidAPI-Host": f"{rapid_api_host}"
        }
        payload: Dict[str, str] = {"link": f"{linkedin_url}"}
        
        response = requests.post(api_endpoint, json=payload, headers=headers)

        try:
            experiences = response.json()['data']['experiences']
            if experiences:
                job_data = experiences[0]
                return cls(title=job_data.get('title'), subtitle=job_data.get('subtitle'), caption=job_data.get('caption'), metadata=job_data.get('metadata'))
            else:
                return cls(title='No job found', subtitle='', caption='', metadata='')
        except Exception as e:
            return cls(title=f"Error parsing JSON: {e}", subtitle='', caption='', metadata='') 
    
    def equals(self, other: 'JobStructure') -> bool:
        return(
            self.title == other.title and
            self.subtitle == other.subtitle and
            self.caption == other.caption and
            self.metadata == other.metadata
        )
