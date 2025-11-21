import requests
from bs4 import BeautifulSoup
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CONFIGURATION ---
URL = "https://www.freejobalert.com/latest-notifications/"
LIMIT_JOBS = 15
MAX_WORKERS = 10
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_age_from_text(text):
    if not text: return 18, 60
    range_match = re.search(r'(\d{2})\s*-\s*(\d{2})', text)
    if range_match: return int(range_match.group(1)), int(range_match.group(2))
    max_match = re.search(r'Max.*?(\d{2})', text, re.IGNORECASE)
    if max_match: return 18, int(max_match.group(1))
    return 18, 60

def clean_text(text):
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def get_job_details(job_data):
    """ Visits the specific job page to find Age, Vacancy, and Apply Links. """
    job_url = job_data['detail_url']
    try:
        resp = requests.get(job_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'lxml')
        
        # Remove script tags to avoid JSON-LD confusion
        for script in soup.find_all('script'):
            script.decompose()
        
        full_text = soup.get_text()
        
        # --- 1. Vacancy Hunt ---
        vacancy_text = "Unknown"
        
        # Strategy 1: Look for "Total Vacancy" in text
        vac_match = re.search(r'Total Vacancy\s*[:\-]?\s*([\d,]+)', full_text, re.IGNORECASE)
        if vac_match:
            vacancy_text = vac_match.group(1)
        else:
            # Strategy 2: Extract from title (e.g., "750 Posts")
            title_match = re.search(r'(\d+)\s*Posts?', job_data['post_name'], re.IGNORECASE)
            if title_match:
                vacancy_text = title_match.group(1)
            else:
                # Strategy 3: Look in full text for "X Posts"
                posts_match = re.search(r'(\d+)\s*Posts?', full_text, re.IGNORECASE)
                if posts_match:
                    vacancy_text = posts_match.group(1)
        
        # --- 2. Age Limit ---
        min_age, max_age = 18, 60
        age_section = soup.find(string=re.compile("Age Limit", re.IGNORECASE))
        if age_section:
            parent = age_section.find_parent()
            if parent:
                parent_text = parent.get_text()
                if len(parent_text.strip()) < 15:
                    next_sibling = parent.find_next_sibling()
                    if next_sibling: parent_text = next_sibling.get_text()
                    else:
                        next_td = parent.find_next('td')
                        if next_td: parent_text = next_td.get_text()
                min_age, max_age = extract_age_from_text(parent_text)

        # --- 3. Link Extraction (The Fix) ---
        apply_link = job_url 
        notification_link = job_url 
        
        # Find all links with "Click here" or "Click Here"
        all_links = soup.find_all('a', href=True)
        
        # Filter to avoid social media and app store links
        skip_domains = ['telegram', 'whatsapp', 'play.google', 'arattai', 'freejobalert.com']
        
        for link in all_links:
            link_text = link.get_text().strip().lower()
            href = link['href']
            
            # Handle relative URLs
            if href.startswith('/'):
                href = "https://www.freejobalert.com" + href
            
            # Skip unwanted domains
            if any(domain in href.lower() for domain in skip_domains):
                continue
            
            # Strategy: First "Click here" is usually notification PDF
            # Second "Click here" is usually the official website (apply link)
            if link_text == "click here":
                if ".pdf" in href.lower():
                    notification_link = href
                elif apply_link == job_url:
                    # Take the first valid external link as apply link
                    apply_link = href
                    print(f"   Found Apply Link: {apply_link}")

        # --- 4. Data Structuring ---
        # Smart Qualification Codes
        qual_codes = []
        q_lower = job_data['original_qual_text'].lower()
        if "10th" in q_lower or "matric" in q_lower: qual_codes.append("10TH")
        if "12th" in q_lower or "inter" in q_lower: qual_codes.append("12TH")
        if "degree" in q_lower or "graduate" in q_lower: qual_codes.append("GRADUATE")
        if "b.tech" in q_lower or "engineering" in q_lower: qual_codes.append("B.TECH")
        if "pg" in q_lower or "post graduate" in q_lower or "mba" in q_lower: qual_codes.append("PG")
        if not qual_codes: qual_codes.append("ANY")
        
        # Display Title
        display_title = f"{job_data['post_name']} | {vacancy_text} Posts"

        # Update job data
        job_data['display_title'] = display_title
        job_data['qualification_codes'] = qual_codes
        job_data['min_age'] = min_age
        job_data['max_age'] = max_age
        job_data['apply_link'] = apply_link
        job_data['notification_link'] = notification_link
        job_data['metadata'] = {
            "total_vacancy": vacancy_text,
            "previous_cutoff": "Data not available"
        }
        
        return job_data

    except Exception as e:
        print(f"Error scraping detail {job_url}: {e}")
        # Defaults
        job_data['display_title'] = f"{job_data['post_name']} | Unknown Posts"
        job_data['qualification_codes'] = ["ANY"]
        job_data['min_age'] = 18
        job_data['max_age'] = 60
        job_data['apply_link'] = job_url
        job_data['notification_link'] = job_url
        job_data['metadata'] = {"total_vacancy": "Unknown", "previous_cutoff": "Data not available"}
        return job_data

def scrape_main_page():
    print(f"🚀 Scraping {URL} with {MAX_WORKERS} threads...")
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        tables = soup.find_all('table', class_='lattbl')
        initial_jobs = []
        count = 0
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    post_name = cols[2].get_text(strip=True)
                    qualification_raw = cols[3].get_text(strip=True)
                    link_tag = cols[-1].find('a', href=True)
                    if not link_tag: continue
                    detail_url = link_tag['href']
                    
                    if count >= LIMIT_JOBS: break
                    
                    job = {
                        "id": str(count),
                        "post_name": post_name,
                        "original_qual_text": qualification_raw,
                        "detail_url": detail_url,
                        # Pre-fill required fields for engine
                        "qualification": [], # Will be filled by deep scraper logic mapping
                        "category_relaxations": {"OBC": 3, "SC": 5, "ST": 5}
                    }
                    initial_jobs.append(job)
                    count += 1
            if count >= LIMIT_JOBS: break
            
        print(f"Found {len(initial_jobs)} jobs. Starting parallel deep scrape...")
        
        final_jobs = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_job = {executor.submit(get_job_details, job): job for job in initial_jobs}
            for future in as_completed(future_to_job):
                try:
                    data = future.result()
                    # Map qualification_codes back to 'qualification' for engine compatibility
                    engine_qual = []
                    for q in data['qualification_codes']:
                        if q == "PG": engine_qual.append("POST GRADUATE")
                        elif q == "ANY": engine_qual.append("ANY_DEGREE")
                        else: engine_qual.append(q)
                    data['qualification'] = engine_qual
                    
                    final_jobs.append(data)
                    print(f"   ✅ Scraped: {data['display_title'][:50]}...")
                except Exception as exc:
                    print(f"   ❌ Job generated an exception: {exc}")

        with open("jobs.json", "w") as f:
            json.dump(final_jobs, f, indent=4)
        print(f"🎉 Saved {len(final_jobs)} jobs to jobs.json!")
        
    except Exception as e:
        print(f"Error in main scraper: {e}")

if __name__ == "__main__":
    start_time = time.time()
    scrape_main_page()
    print(f"Total time: {time.time() - start_time:.2f} seconds")
