from requests import get
from dotenv import load_dotenv
import os
import json

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
FULL_TIME = "1"
JOB_TITLES = ["ai engineer", "ml engineer", "mlops", "data engineer"] # "what" field for API
LOCATIONS = ["gold coast", "brisbane"]

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

def search_and_display_jobs():
    """This function searches jobs from 4 job titles in the AI field and 2 locations. Then displays them to the user. It also returns a list of job dictionaries that were found."""
    
    # Request Search
    index = 1
    job_list = []
    # Conduct all 8 job searches
    for location in LOCATIONS:
        for job_title in JOB_TITLES:
            jobs = fetch_jobs(location, job_title) # pull jobs from Adzuna API
            for job in jobs:
                job_data = extract_job_data(job) # extract the data we want to display
                display_job(job_data, index) # display the data in a readable format
                job_list.append(job_data) # store jobs that were displayed in memory for further use.
                index += 1
    return job_list

def save_jobs(jobs_to_save):
    """This function takes a list of job dictionaries and saves them to a file. If jobs have been saved in the past the function adds the new jobs to the exisiting saved list."""

    # Get jobs already saved if any.
    old_saved_jobs = load_saved_jobs()
    saved_jobs = old_saved_jobs + jobs_to_save # add new saved jobs to existing saved jobs
    with open("saved_jobs.json", "w") as f:
        json.dump(saved_jobs, f, indent = 2)
    print(f"\nSuccessfully added {len(jobs_to_save)} jobs.") # confirm with the user how many jobs were saved.
    return

def load_saved_jobs():
    """This function gets saved jobs from the saved_jobs.json file and returns it as a list of jobs dictionaries."""

    try:
        with open("saved_jobs.json", "r") as f:
            saved_jobs = json.load(f)
    except FileNotFoundError:
        saved_jobs = []

    return saved_jobs

def select_jobs(current_jobs):
    """This function asks the user for a list of jobs to save and returns the list of those jobs."""
    
    selected_jobs = []
    print("\nEnter a sequence of job numbers separated by commas like so: 1, 4, 7, 5")
    job_indexes = input("\nJobs you want to save: ").strip() # get job numbers from user
    try:
        # Parse job numbers
        job_indexes = job_indexes.split(",")
        for job_index in job_indexes:
            job_index = int(job_index.strip())
            if job_index >= 1 and job_index <= len(current_jobs):
                selected_jobs.append(current_jobs[job_index-1]) # store the jobs to be saved
            else:
                print(f"\nJob #{job_index} does not exist and was not saved. Please ensure you enter job numbers in the above list in future.")
    except ValueError:
        print("\nInvalid input. Please enter numbers separated by commas.\n")
    return selected_jobs


# Greeting    
print("\n-------------------------------------------------------------")
print("Welcome to your Job Aggregator!")
print("You can search jobs in your field and save the ones you like.")
print("-------------------------------------------------------------\n")
current_jobs = []
while True:
    # Main menu
    print("Enter the number that corresponds with one of the following options:")
    print("\n1. Search Jobs")
    if current_jobs:
        print("2. Save Jobs")
    else:
        print("2. Save Jobs (Not Available. Search Jobs First)")
    print("3. List Saved Jobs")
    print("4. Quit")

    choice = input("\nChoice: ").strip() # get input
    # Handle menu choices
    if choice == "1": # Search Jobs
        print("\nJobs Found:\n")
        current_jobs = search_and_display_jobs()
    elif choice == "2": # Save Jobs
        if current_jobs: 
            selected_jobs = select_jobs(current_jobs) # let user select the jobs they want to save
            if selected_jobs:
                save_jobs(selected_jobs) # save jobs
        else: # No jobs have been searched so can't save anything
            print("\nPlease search some jobs first, there is nothing to save in this session.\n")
    elif choice == "3": # List Saved Jobs
        saved_jobs = load_saved_jobs()
        if saved_jobs:
            # display them
            print("\nSaved Jobs:\n")
            for index, job in enumerate(saved_jobs, 1):
                display_job(job, index)
        else:
            print("\nNo saved jobs to display. Search and save some jobs before using this option.\n")
    elif choice == "4": # Quit
        print("\nClosing...")
        exit(0)
    else:
        print("\nInvalid input, please enter one of the option numbers listed.\n")