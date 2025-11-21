# Reddit Post for r/developersIndia

## Title
I built a "Reverse Job Search" engine for Indian Govt Exams using FastAPI (Open Source + Live Demo)

## Body

Hey r/developersIndia! 👋

I wanted to share a project I built to solve a problem that's been frustrating me (and probably millions of others) for years.

### The Pain 😤

If you've ever applied for government jobs in India, you know the drill:

1. Open FreeJobAlert
2. Click through 50+ job notifications
3. Download each PDF to check age limits
4. Manually calculate if you're eligible (OBC +3 years, SC/ST +5 years)
5. Search for the "Apply Online" link buried somewhere in the notification
6. Realize you're overage by 2 months 🤦‍♂️

**Hours wasted. Opportunities missed.**

### The Solution 💡

I built **SarkariMatch** - a "reverse job search" engine that flips the script:

Instead of you searching through jobs, **the jobs come to you**.

**How it works:**
- Enter your DOB, category (OBC/SC/ST), and qualification
- Get a clean dashboard showing **ONLY** jobs you're eligible for
- See vacancy count, age limits, and direct apply buttons
- Click "Direct Apply" to go straight to the official portal (no more PDF hunting!)

### The Stack 🛠️

- **Backend:** FastAPI (Python 3.10+)
- **Scraping:** BeautifulSoup4 + Requests with ThreadPoolExecutor
- **Frontend:** Jinja2 templates + Tailwind CSS
- **Deployment:** Heroku (for demo)

**Performance:**
- Scrapes 15 jobs in ~3 seconds using parallel processing
- Extracts vacancy numbers, age limits, and direct application links
- Filters out social media links (Telegram/WhatsApp spam)

### Live Demo 🎥

**Try it here:** [Your Heroku URL]

*(Note: Free tier, might take 10 seconds to wake up from sleep)*

**Screenshots:**

[Homepage]
![Homepage](https://github.com/amnindersingh12/sarkari_match/raw/main/screenshots/homepage.png)

[Results Dashboard]
![Dashboard](https://github.com/amnindersingh12/sarkari_match/raw/main/screenshots/dashboard.png)

### The Challenge 🤔

The hardest part was writing robust regex patterns to extract data from inconsistent HTML structures. Some notifications have "Total Vacancy" in a table, others in plain text, and some don't mention it at all.

**This is where I need help!**

### Open Source 🌟

**GitHub:** https://github.com/amnindersingh12/sarkari_match

MIT licensed. PRs welcome!

**Looking for contributors to help with:**
- Improving regex patterns for better data extraction
- Adding support for other job portals (SarkariResult, Employment News)
- Extracting physical standards for police/defense jobs
- Parsing exam dates and admit card notifications
- Adding previous year cutoff data

### Why I Built This 🎯

I've seen too many talented people miss opportunities because they didn't know they were eligible. Government job notifications are intentionally complex, and the application process shouldn't be.

This tool won't guarantee you a job, but it'll save you hours of manual work and ensure you never miss an opportunity you qualify for.

### Tech Highlights 🔧

- **Multi-strategy vacancy extraction** (Total Vacancy text → title → full text)
- **Smart link filtering** (skips Telegram, WhatsApp, internal redirects)
- **Category-based age relaxations** (automatic OBC/SC/ST calculations)
- **Parallel scraping** with ThreadPoolExecutor for speed

---

**Demo:** [Your Heroku URL]  
**GitHub:** https://github.com/amnindersingh12/sarkari_match  
**Stack:** Python, FastAPI, BeautifulSoup4, Jinja2, Tailwind CSS

Let me know what you think! Happy to answer any questions about the implementation. 🚀

---

*Note: This is for educational purposes. Always verify eligibility from official notifications before applying.*

---

# Reddit Post for r/Python

## Title
Built a web scraper that extracts government job data and matches eligibility (FastAPI + BeautifulSoup + Live Demo)

## Body

Hey r/Python! 👋

I built a web scraping project that solves a real problem for millions of job seekers in India.

### The Problem

Government job portals in India (like FreeJobAlert) list hundreds of jobs, but checking eligibility is manual and time-consuming. You have to:
- Click through each job notification
- Download PDFs to check age limits
- Calculate category-based relaxations
- Find the actual application link

### The Solution

**SarkariMatch** - A FastAPI app that:
1. Scrapes FreeJobAlert using BeautifulSoup4
2. Extracts vacancy numbers, age limits, and direct application links
3. Filters jobs based on user's age, category, and qualification
4. Shows only eligible jobs with direct apply buttons

### Technical Implementation 🔧

**Scraping Strategy:**
```python
# Multi-strategy vacancy extraction
vac_match = re.search(r'Total Vacancy\s*[:\-]?\s*([\d,]+)', full_text, re.IGNORECASE)
if not vac_match:
    # Fallback to title extraction
    title_match = re.search(r'(\d+)\s*Posts?', job_data['post_name'], re.IGNORECASE)
```

**Parallel Processing:**
```python
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_job = {executor.submit(get_job_details, job): job for job in initial_jobs}
    for future in as_completed(future_to_job):
        data = future.result()
```

**Smart Link Filtering:**
```python
skip_domains = ['telegram', 'whatsapp', 'play.google', 'arattai', 'freejobalert.com']
# Prioritizes first valid external "Click here" link
```

### Performance 📊

- **Speed:** 15 jobs in ~3 seconds
- **Accuracy:** Multi-strategy extraction with fallbacks
- **Reliability:** Error handling for timeouts and missing data

### Live Demo 🎥

**Try it:** [Your Heroku URL]

**GitHub:** https://github.com/amnindersingh12/sarkari_match

### Challenges & Learnings 🤔

1. **Inconsistent HTML structures** - Solved with multi-strategy extraction
2. **Social media link spam** - Implemented domain filtering
3. **Timeout handling** - Added fallbacks and default values
4. **Parallel scraping** - Used ThreadPoolExecutor for 5x speed improvement

### Stack

- Python 3.10+
- FastAPI (web framework)
- BeautifulSoup4 + lxml (scraping)
- Requests (HTTP)
- Jinja2 (templating)
- Tailwind CSS (UI)

### Open Source 🌟

MIT licensed. Looking for contributors to help with:
- Improving regex patterns
- Adding new job portals
- Extracting additional data fields

---

**Demo:** [Your Heroku URL]  
**GitHub:** https://github.com/amnindersingh12/sarkari_match

Let me know if you have questions about the scraping logic or FastAPI implementation! 🚀

---

# Reddit Post for r/india

## Title
Made a free tool that shows government jobs you're actually eligible for (saves hours of PDF reading)

## Body

Hey r/india! 👋

If you or anyone you know has applied for government jobs, you know how painful it is to check eligibility for each notification.

### The Problem

FreeJobAlert lists 50+ jobs daily. For each job, you need to:
- Download the PDF notification
- Check if you meet the age limit
- Calculate category relaxation (OBC +3 years, SC/ST +5 years)
- Find the "Apply Online" link
- Realize you're overage by 2 months 😭

**Hours wasted every day.**

### The Solution

I built **SarkariMatch** - a free tool that does this automatically.

**How it works:**
1. Enter your Date of Birth
2. Select your category (General/OBC/SC/ST)
3. Select your qualification (10th/12th/Graduate/B.Tech/PG)
4. Get a list of **ONLY** jobs you're eligible for

**Features:**
- ✅ Shows total vacancy count
- ✅ Displays age limit with your relaxation
- ✅ Direct "Apply Online" button (no PDF hunting!)
- ✅ Updates daily with latest jobs

### Live Demo

**Try it here:** [Your Heroku URL]

*(Free to use, no registration required)*

### Why I Built This

I've seen talented people miss opportunities because they didn't know they were eligible. Government notifications are complex by design, but checking eligibility shouldn't be.

This won't guarantee you a job, but it'll save you hours and ensure you never miss an opportunity.

### Open Source

The code is on GitHub: https://github.com/amnindersingh12/sarkari_match

If you're a developer and want to contribute (or just curious how it works), check it out!

---

**Try it:** [Your Heroku URL]  
**GitHub:** https://github.com/amnindersingh12/sarkari_match

Hope this helps someone! Let me know if you have suggestions. 🙏

---

*Disclaimer: Always verify eligibility from official notifications before applying.*
