# Contributing to SarkariMatch

Thank you for your interest in contributing to SarkariMatch! This document will help you get started.

## 🏗️ Project Architecture

### Core Components

1. **`scraper.py`** - The Data Extraction Layer
   - Fetches job listings from FreeJobAlert
   - Performs deep scraping on individual job pages
   - Extracts structured data (vacancy, age, links)
   - Outputs to `jobs.json`

2. **`main.py`** - The Matching Engine & API
   - FastAPI application
   - `/` - Serves the input form
   - `/match` - Processes user input and returns eligible jobs
   - Age calculation with category relaxations
   - Qualification matching logic

3. **`templates/`** - The User Interface
   - `index.html` - Input form (DOB, Category, Qualification)
   - `results.html` - Job results dashboard with cards

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/yourusername/sarkari_match.git
cd sarkari_match
```

### 2. Set Up Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
# Scrape fresh data
python scraper.py

# Start the server
uvicorn main:app --reload
```

### 4. Make Your Changes

Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

## 📝 Common Contribution Scenarios

### Adding a New Regex Pattern for Job Titles

**Problem:** Some job titles aren't being parsed correctly.

**Solution:** Update the qualification extraction logic in `scraper.py`.

**Example:**
```python
# In get_job_details() function, around line 105
qual_codes = []
q_lower = job_data['original_qual_text'].lower()

# Add your new pattern here
if "diploma" in q_lower:
    qual_codes.append("DIPLOMA")
```

### Improving Vacancy Extraction

**Location:** `scraper.py`, `get_job_details()` function, around line 45

**Current Logic:**
```python
# Strategy 1: Look for "Total Vacancy" in text
vac_match = re.search(r'Total Vacancy\s*[:\-]?\s*([\d,]+)', full_text, re.IGNORECASE)

# Strategy 2: Extract from title
title_match = re.search(r'(\d+)\s*Posts?', job_data['post_name'], re.IGNORECASE)
```

**To Add a New Pattern:**
```python
# Strategy 4: Your new pattern
your_match = re.search(r'YOUR_REGEX_HERE', full_text)
if your_match:
    vacancy_text = your_match.group(1)
```

### Adding a New Data Field

**Example:** Extract "Last Date to Apply"

1. **Update Scraper** (`scraper.py`):
```python
# In get_job_details()
last_date = "Not specified"
date_match = re.search(r'Last Date.*?(\d{2}-\d{2}-\d{4})', full_text, re.IGNORECASE)
if date_match:
    last_date = date_match.group(1)

job_data['metadata']['last_date'] = last_date
```

2. **Update UI** (`templates/results.html`):
```html
<div>
    <p class="text-xs font-medium text-gray-500 uppercase">Last Date</p>
    <p class="text-lg font-semibold text-gray-900 mt-1">{{ job.metadata.last_date }}</p>
</div>
```

### Adding a New Job Portal

1. Create a new scraper function in `scraper.py`:
```python
def scrape_sarkari_result():
    # Your scraping logic here
    pass
```

2. Merge results with existing data:
```python
fja_jobs = scrape_main_page()
sr_jobs = scrape_sarkari_result()
all_jobs = fja_jobs + sr_jobs
```

## 🎨 Code Style Guide

### Python Code
- **Formatter:** Use [Black](https://github.com/psf/black) with default settings
  ```bash
  pip install black
  black scraper.py main.py
  ```
- **Line Length:** 100 characters max
- **Imports:** Group by standard library, third-party, local
- **Docstrings:** Use for all functions
  ```python
  def extract_age_from_text(text):
      """
      Extracts min and max age from text using regex patterns.
      
      Args:
          text (str): Text containing age information
          
      Returns:
          tuple: (min_age, max_age)
      """
  ```

### HTML/CSS
- Use Tailwind CSS utility classes
- Keep templates readable with proper indentation
- Add comments for complex sections

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(scraper): add support for SarkariResult portal
fix(ui): correct age calculation for leap years
docs(readme): update installation instructions
refactor(engine): simplify qualification matching logic
```

## 🧪 Testing

Currently, we don't have automated tests (PRs welcome!). Please manually test:

1. **Scraper:** Run `python scraper.py` and verify `jobs.json` is generated
2. **Engine:** Test with different DOB/Category/Qualification combinations
3. **UI:** Check responsiveness on mobile and desktop

## 📋 Pull Request Process

1. **Update Documentation:** If you add features, update README.md
2. **Test Thoroughly:** Ensure your changes don't break existing functionality
3. **Describe Your Changes:** Write a clear PR description
4. **Link Issues:** Reference any related issues

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test this?

## Screenshots (if applicable)
Add screenshots for UI changes.
```

## 🐛 Reporting Bugs

Use GitHub Issues with the following template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior.

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. macOS, Ubuntu]
- Python version: [e.g. 3.10]
- Browser: [e.g. Chrome, Firefox]
```

## 💡 Feature Requests

We love new ideas! Open an issue with:
- **Problem:** What problem does this solve?
- **Solution:** Your proposed solution
- **Alternatives:** Any alternative solutions you considered

## 🎯 Good First Issues

Look for issues labeled `good-first-issue` - these are great for newcomers!

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Chat:** (Add Discord/Slack link if you create one)

## 🙏 Thank You!

Every contribution, no matter how small, makes a difference. Thank you for helping make SarkariMatch better!

---

**Happy Contributing! 🚀**
