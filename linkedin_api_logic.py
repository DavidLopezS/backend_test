import requests

access_token: str = "API_TOKEN"
api_endpoint: str = "temp"

def detect_job_change(linkedin_url: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        'linkedin_porfile_url': f"{linkedin_url}",
        'use-cache': 'if-recent'
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    return f"New job detected: {response.json()['experiences'][0]['title']}" 