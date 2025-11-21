from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from datetime import date, datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SarkariMatch")
templates = Jinja2Templates(directory="templates")

# Load jobs from JSON
def load_jobs():
    try:
        with open("jobs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("jobs.json not found. Run scraper.py first.")
        return []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/match", response_class=HTMLResponse)
async def match_jobs(
    request: Request,
    dob: str = Form(...),
    category: str = Form(...),
    qualification: str = Form(...)
):
    jobs = load_jobs()
    eligible_jobs = []
    
    # Calculate Age
    dob_date = date.fromisoformat(dob)
    today = date.today()
    user_age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    
    for job in jobs:
        # 1. Age Check with Relaxation
        relaxation = 0
        if category == "OBC":
            relaxation = job["category_relaxations"].get("OBC", 0)
        elif category in ["SC", "ST"]:
            relaxation = job["category_relaxations"].get("SC", 0) # Assuming SC/ST same
            
        effective_max_age = job["max_age"] + relaxation
        
        is_age_eligible = user_age <= effective_max_age
        
        # 2. Qualification Check
        # Check if selected qualification is in job's list OR job allows ANY_DEGREE
        # Also, higher degrees typically imply lower ones, but for strict matching we check list.
        # User selection: 10th, 12th, Graduate, B.Tech, Post Graduate
        # Job tags: 10TH, 12TH, GRADUATE, B.TECH, POST GRADUATE, ANY_DEGREE
        
        user_qual_map = {
            "10th": "10TH",
            "12th": "12TH",
            "Graduate": "GRADUATE",
            "B.Tech": "B.TECH",
            "Post Graduate": "POST GRADUATE"
        }
        
        user_q_tag = user_qual_map.get(qualification, "")
        
        # Logic: If user has B.TECH, they are also GRADUATE, 12TH, 10TH.
        # We need a hierarchy.
        hierarchy = ["10TH", "12TH", "GRADUATE", "B.TECH", "POST GRADUATE"]
        # Note: B.TECH is a type of GRADUATE, but for this simple logic let's treat them as tags.
        # If job requires 10TH, and user is B.TECH, they are eligible.
        
        # Let's simplify: Check if job requirement is present in user's "implied" qualifications.
        user_implied_quals = set()
        if user_q_tag == "10TH": user_implied_quals.update(["10TH"])
        elif user_q_tag == "12TH": user_implied_quals.update(["10TH", "12TH"])
        elif user_q_tag == "GRADUATE": user_implied_quals.update(["10TH", "12TH", "GRADUATE"])
        elif user_q_tag == "B.TECH": user_implied_quals.update(["10TH", "12TH", "GRADUATE", "B.TECH"])
        elif user_q_tag == "POST GRADUATE": user_implied_quals.update(["10TH", "12TH", "GRADUATE", "B.TECH", "POST GRADUATE"]) # Assuming PG implies others for simplicity
        
        is_qual_eligible = False
        if "ANY_DEGREE" in job["qualification"]:
            is_qual_eligible = True
        else:
            # Check if ANY of the job's requirements match the user's implied quals
            for req in job["qualification"]:
                if req in user_implied_quals:
                    is_qual_eligible = True
                    break
        
        if is_age_eligible and is_qual_eligible:
            job["effective_max_age"] = effective_max_age
            job["relaxation_applied"] = relaxation
            eligible_jobs.append(job)

    return templates.TemplateResponse("results.html", {
        "request": request, 
        "jobs": eligible_jobs,
        "user_age": user_age,
        "count": len(eligible_jobs)
    })
