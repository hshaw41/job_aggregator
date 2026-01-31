from requests import get
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Auth Vars
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Base url
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"

# Search Params
COUNTRY = "au"
PAGE = "1"
RESULTS_PER_PAGE = 5
SORT_DIRECTION = "up"
SORT_BY = "date"
FULL_TIME = "1"

def fetch_jobs(location, job_title):
    """This function fetches the top five jobs by job title and location. Returns a list of raw job result dictionaries"""
    
    job_search_endpoint = f"/jobs/{COUNTRY}/search/{PAGE}" # set the endpoint
    url = ADZUNA_BASE_URL + job_search_endpoint # construct full url with base.

    try:
        response = get(url, params={"app_id":ADZUNA_APP_ID, # Send Request with Params
                                        "app_key":ADZUNA_APP_KEY,
                                        "results_per_page":RESULTS_PER_PAGE,
                                        "what":job_title,
                                        "where":location,
                                        "full_time":FULL_TIME})
        
        # Check request
        if response.ok:
            return response.json()["results"] # Return list of raw jobs
        else:
            print(f"API Error: {response.status_code} - {response.reason}") # print status code 
            return []
    except Exception as error: # Request failed to send. Network error handling.
        print(f"Network error: {error}")
        return []
    
def extract_job_data(raw_job):
    """This function intakes a raw job dictionary from the Adzuna API and extracts key data and returns that in a dict."""

    job_data = {
        "title":raw_job["title"],
        "company": raw_job["company"]["display_name"],
        "location": raw_job["location"]["display_name"],
        "salary_min": raw_job.get("salary_min", 0),
        "salary_max": raw_job.get("salary_max", 0),
        "link": raw_job["redirect_url"],
        "description": raw_job["description"]
    }

    return job_data

def display_job(job_data, index):
    """This function formats a job data object into a readable form and prints it to the CLI."""

    if job_data["salary_min"] and job_data["salary_max"]:
        output = f"{index}. {job_data["title"]} - {job_data["company"]} - {job_data["location"]} - ${job_data["salary_min"]}-{job_data["salary_max"]}\n\"{job_data["description"]}\"\n[Link: {job_data["link"]}]"
    else:
        output = f"{index}. {job_data["title"]} - {job_data["company"]} - {job_data["location"]}\n\"{job_data["description"]}\"\n[Link: {job_data["link"]}]"
    print(output + "\n")

        
job_titles = ["ai engineer", "ml engineer", "mlops", "data engineer"] # "what" field for API
locations = ["gold coast", "brisbane"]

# Request Search
index = 1
for location in locations:
    for job_title in job_titles:
        jobs = fetch_jobs(location, job_title)
        for job in jobs:
            job_data = extract_job_data(job)
            display_job(job_data, index)
            index += 1