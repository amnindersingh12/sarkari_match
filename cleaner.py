from typing import List

def normalize_qualification(raw_text: str) -> List[str]:
    """
    Normalizes qualification text into a standard list of degrees.
    Uses simple keyword matching for now.
    """
    if not raw_text:
        return []
    
    raw_text = raw_text.lower()
    normalized = []
    
    # Keyword matching logic
    keywords = {
        "10th": "10th",
        "matric": "10th",
        "ssc": "10th",
        "12th": "12th",
        "hsc": "12th",
        "intermediate": "12th",
        "b.tech": "B.Tech",
        "b.e": "B.Tech", # Mapping B.E to B.Tech for simplicity or keep separate
        "graduate": "Graduate",
        "degree": "Graduate",
        "diploma": "Diploma",
        "mba": "MBA",
        "pg": "Post Graduate",
        "post graduate": "Post Graduate"
    }
    
    for key, value in keywords.items():
        if key in raw_text:
            if value not in normalized:
                normalized.append(value)
                
    # TODO: Integrate Gemini API for advanced parsing
    # def parse_with_gemini(text):
    #     prompt = f"Extract qualifications from: {text}"
    #     # call gemini
    #     return result
    # if not normalized:
    #     normalized = parse_with_gemini(raw_text)
    
    return normalized

if __name__ == "__main__":
    # Test the cleaner
    test_strings = [
        "Passed 10th Class",
        "Degree/ PG",
        "B.E/ B.Tech",
        "Matriculation"
    ]
    for t in test_strings:
        print(f"Original: '{t}' -> Normalized: {normalize_qualification(t)}")
