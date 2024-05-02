import requests

rapid_api_key: str = "9f5cd37c5bmsh47e1ba15a30b7ecp1f27cfjsn5e640e1ac804"
rapid_api_host: str = "linkedin-data-scraper.p.rapidapi.com"
api_endpoint: str = "https://linkedin-data-scraper.p.rapidapi.com/person"

def detect_job_change(linkedin_url: str):
    
    headers = {
        "content-type": "application/json",
	    "X-RapidAPI-Key": f"{rapid_api_key}",
	    "X-RapidAPI-Host": f"{rapid_api_host}"}
    
    payload = {"link": f"{linkedin_url}"}
    response = requests.post(api_endpoint, json=payload, headers=headers)
    return f"New job detected: {response.json()['data']['experiences'][0]['title']}" 