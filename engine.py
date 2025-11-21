from datetime import date
from typing import Dict, Any
from models import UserProfile, JobPost, Category

def calculate_age(dob: date) -> int:
    """
    Calculates age from DOB to today.
    """
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def check_eligibility(user: UserProfile, job: JobPost) -> Dict[str, Any]:
    """
    Checks if a user is eligible for a job based on age and other criteria.
    """
    reasons = []
    eligible = True
    
    # 1. Age Check
    user_age = calculate_age(user.dob)
    
    # Determine relaxation
    relaxation = 0
    if user.category.value in job.age_relaxation_rules:
        relaxation = job.age_relaxation_rules[user.category.value]
    elif user.category.name in job.age_relaxation_rules: # Handle case where enum name is used in dict
        relaxation = job.age_relaxation_rules[user.category.name]
        
    effective_max_age = job.max_age + relaxation
    
    if user_age < job.min_age:
        eligible = False
        reasons.append(f"Ineligible: Age {user_age} is below minimum age {job.min_age}.")
    elif user_age > effective_max_age:
        eligible = False
        reasons.append(f"Ineligible: Age {user_age} exceeds limit {effective_max_age} ({job.max_age} + {relaxation} {user.category.value} relaxation).")
    else:
        reasons.append(f"Eligible: Age {user_age} is within limit {effective_max_age} ({job.max_age} + {relaxation} {user.category.value} relaxation).")
        
    # 2. Degree Check (Simple string match for now, can be improved)
    # If job has a required degree, check if user has it.
    if job.required_degree:
        # Normalize strings for comparison
        user_degrees_norm = [d.lower().strip() for d in user.degrees]
        job_degree_norm = job.required_degree.lower().strip()
        
        # Check if any user degree matches or contains the job degree
        # This is a basic check. In reality, it would be more complex hierarchy.
        degree_match = False
        for d in user_degrees_norm:
            if job_degree_norm in d or d in job_degree_norm:
                degree_match = True
                break
        
        if not degree_match:
             # We won't make it strictly ineligible for now as string matching is flaky, 
             # but we can add a warning or make it ineligible if strict.
             # Let's make it a reason but maybe not hard fail if we want to be lenient with raw text.
             # However, prompt implies "Matching Engine", so let's be strict if we can.
             # Given "Qualification" is raw text, strict matching is dangerous.
             # Let's just add a note.
             reasons.append(f"Note: Job requires '{job.required_degree}', User has {user.degrees}. Verification needed.")
        else:
             reasons.append(f"Eligible: Degree matches '{job.required_degree}'.")

    return {
        "eligible": eligible,
        "reasons": reasons,
        "job_id": job.id,
        "job_title": job.title
    }
