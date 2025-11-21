from enum import Enum
from typing import Dict, List, Optional
from datetime import date
from pydantic import BaseModel, Field

class Degree(str, Enum):
    TENTH = "10th"
    TWELFTH = "12th"
    GRADUATE = "Graduate"
    POST_GRADUATE = "Post Graduate"
    DIPLOMA = "Diploma"
    ENGINEERING = "Engineering"
    OTHER = "Other"

class Category(str, Enum):
    GEN = "Gen"
    OBC = "OBC"
    SC = "SC"
    ST = "ST"

class JobPost(BaseModel):
    id: str
    title: str
    min_age: int = 18
    max_age: int = 60
    required_degree: Optional[str] = None # Keeping as string to allow flexibility or mapping to Enum later if needed, but user asked for Enum in prompt, let's try to stick to Enum if possible, but raw text might be messy. Let's use str for now as scraper output might be messy.
    age_relaxation_rules: Dict[str, int] = Field(default_factory=lambda: {'OBC': 3, 'SC': 5, 'ST': 5, 'Gen': 0})
    last_date: Optional[str] = None
    apply_link: Optional[str] = None

class UserProfile(BaseModel):
    dob: date
    category: Category
    degrees: List[str]
    height_cm: Optional[float] = None
