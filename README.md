# Job Aggregator CLI

## What it does
A CLI tool that searches and saves job listings from Adzuna API. Searches for AI/ML roles (AI Engineer, ML Engineer, MLOps, Data Engineer) in Gold Coast and Brisbane.

## Prerequisites
- Python 3.13
- Adzuna API account (free tier works fine)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hshaw41/job-aggregator.git
cd job-aggregator
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Adzuna API credentials:
```
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

Get your API keys by signing up at [Adzuna Developer Portal](https://developer.adzuna.com/signup).

5. Run the program:
```bash
python3 job_search.py
```

## Usage
Run the program and select a menu option:

**1. Search Jobs** - Fetches current AI/ML job listings from Adzuna  
**2. Save Jobs** - Save specific jobs by entering comma-separated numbers (e.g., `1, 4, 7`). Only available after searching.  
**3. List Saved Jobs** - View all previously saved jobs  
**4. Quit** - Exit the program

## How it works
1. Job Search
The script makes 8 API requests total. One for each of the 4 job titles "ai engineer", "ml engineer", "mlops", "data engineer", for each location "Gold Coast", "Brisbane". The API request returns only jobs in australia. The script returns at maximum 5 jobs for each API call so 40 is the maximum total jobs listed at once.

2. Job Saving
The script parses the list of jobs the user wants to save and stores the actual list of those job objects in a json file called "saved_jobs.json". Each job object is a dictionary containing the title, company, location, salary (if available), link and description of each job. This is saved to a json file using the json built in python library. Saved jobs are accumulated by loading exisiting ones in the file and concatenating them with the new jobs to be saved by the user and overwrites the file with the full list.

## Post-MVP / Future Plans
-  Remove jobs from saved list via CLI
-  Add Indeed API as a second data source
-  Add additional job board APIs (Remote OK, JSearch, etc.)
-  De-duplicate the saved job list, don't let the user save the same job twice.

## Tech Stack
- Python
- requests
- python-dotenv