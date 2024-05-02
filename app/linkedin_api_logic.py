import requests
import os
from app.classes import JobStructure

rapid_api_key: str = os.environ.get('X_RAPID_API_KEY', '')
rapid_api_host: str = os.environ.get('X_RAPID_API_HOST', '')
api_endpoint: str = os.environ.get('URL', '')



def fetch_linkedin_profile(linkedin_url: str):
    headers = {
        "content-type": "application/json",
	    "X-RapidAPI-Key": f"{rapid_api_key}",
	    "X-RapidAPI-Host": f"{rapid_api_host}"
    }
    payload = {"link": f"{linkedin_url}"}
    
    response = requests.post(api_endpoint, json=payload, headers=headers)

    try:
        job_structure: JobStructure
        experiences = response.json()['data']['experiences']
        if experiences:
            job_structure()
        
    except Exception as e:
        return e 