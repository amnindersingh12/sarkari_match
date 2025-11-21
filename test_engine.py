from datetime import date
from models import UserProfile, JobPost, Category
from engine import check_eligibility

def test_engine():
    # Test Case 1: Eligible User
    user1 = UserProfile(
        dob=date(1998, 1, 1), # 26 years old approx (in 2024)
        category=Category.OBC,
        degrees=["B.Tech", "10th", "12th"]
    )
    
    job1 = JobPost(
        id="1",
        title="Software Engineer",
        min_age=21,
        max_age=25,
        age_relaxation_rules={'OBC': 3, 'SC': 5, 'Gen': 0}, # Max age for OBC = 28
        required_degree="B.Tech"
    )
    
    result1 = check_eligibility(user1, job1)
    print(f"Test 1 (Should be Eligible): {result1['eligible']}")
    print(f"Reasons: {result1['reasons']}")
    
    # Test Case 2: Ineligible User (Age)
    user2 = UserProfile(
        dob=date(1990, 1, 1), # 34 years old approx
        category=Category.GEN,
        degrees=["B.Tech"]
    )
    
    job2 = JobPost(
        id="2",
        title="Junior Engineer",
        min_age=18,
        max_age=30,
        age_relaxation_rules={'OBC': 3, 'SC': 5, 'Gen': 0} # Max age for Gen = 30
    )
    
    result2 = check_eligibility(user2, job2)
    print(f"\nTest 2 (Should be Ineligible - Age): {result2['eligible']}")
    print(f"Reasons: {result2['reasons']}")

    # Test Case 3: Ineligible User (Degree - Warning)
    user3 = UserProfile(
        dob=date(2000, 1, 1), 
        category=Category.SC,
        degrees=["12th"]
    )
    
    job3 = JobPost(
        id="3",
        title="Senior Scientist",
        min_age=18,
        max_age=40,
        required_degree="PhD"
    )
    
    result3 = check_eligibility(user3, job3)
    print(f"\nTest 3 (Should be Eligible but with Degree Warning): {result3['eligible']}")
    print(f"Reasons: {result3['reasons']}")

if __name__ == "__main__":
    test_engine()
