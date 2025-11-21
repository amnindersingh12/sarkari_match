from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from datetime import date, datetime
import os

app = FastAPI(title="SarkariMatch")
templates = Jinja2Templates(directory="templates")

# Load jobs from JSON
def load_jobs():
    """Load jobs from jobs.json, create empty file if doesn't exist"""
    if not os.path.exists("jobs.json"):
        print("⚠️ jobs.json not found, creating empty file...")
        with open("jobs.json", "w") as f:
            json.dump([], f)
        return []
    
    try:
        with open("jobs.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading jobs.json: {e}")
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
        user_qual_map = {
            "10th": "10TH",
            "12th": "12TH",
            "Graduate": "GRADUATE",
            "B.Tech": "B.TECH",
            "Post Graduate": "POST GRADUATE"
        }
        
        user_q_tag = user_qual_map.get(qualification, "")
        
        # Build user's implied qualifications
        user_implied_quals = set()
        if user_q_tag == "10TH": user_implied_quals.update(["10TH"])
        elif user_q_tag == "12TH": user_implied_quals.update(["10TH", "12TH"])
        elif user_q_tag == "GRADUATE": user_implied_quals.update(["10TH", "12TH", "GRADUATE"])
        elif user_q_tag == "B.TECH": user_implied_quals.update(["10TH", "12TH", "GRADUATE", "B.TECH"])
        elif user_q_tag == "POST GRADUATE": user_implied_quals.update(["10TH", "12TH", "GRADUATE", "B.TECH", "POST GRADUATE"])
        
        is_qual_eligible = False
        if "ANY_DEGREE" in job["qualification"]:
            is_qual_eligible = True
        else:
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
