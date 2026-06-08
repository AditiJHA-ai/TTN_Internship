"""
Week 5 — Resume Analyzer
Uses the OpenAI API to extract structured information from a resume.
Demonstrates: system/user roles, structured JSON output, prompt engineering.
"""
 
import json
from openai import OpenAI
 
client = OpenAI()  # reads OPENAI_API_KEY from environment
 
SYSTEM_PROMPT = """
You are a resume parser. Your job is to extract structured information
from the resume text provided by the user.
 
Always respond with valid JSON only — no markdown, no preamble, no explanation.
Use exactly this schema:
 
{
  "name": "string",
  "email": "string or null",
  "phone": "string or null",
  "location": "string or null",
  "summary": "1-2 sentence summary of the candidate",
  "years_of_experience": number,
  "skills": ["list", "of", "skills"],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "year": "string or null"
    }
  ],
  "experience": [
    {
      "title": "string",
      "company": "string",
      "duration": "string",
      "highlights": ["key achievement or responsibility"]
    }
  ],
  "languages": ["list of languages if mentioned"],
  "suitability_score": number between 1 and 10,
  "suitability_reason": "one sentence explaining the score"
}
 
If a field is not mentioned, use null for strings, 0 for numbers, [] for arrays.
"""
 
SAMPLE_RESUME = """
Priya Sharma
priya.sharma@email.com | +91-9876543210 | Bangalore, India
github.com/priyasharma | linkedin.com/in/priyasharma
 
SUMMARY
Software engineer with 3 years of experience building backend systems and APIs.
Passionate about machine learning and currently transitioning into AI/ML engineering.
 
SKILLS
Python, FastAPI, Django, PostgreSQL, Docker, Git, scikit-learn,
pandas, numpy, REST APIs, SQL, Linux, LangChain (learning)
 
EDUCATION
B.Tech in Computer Science — VIT University, 2021
 
EXPERIENCE
 
Backend Engineer — Infosys, Bangalore (Jan 2022 – Present)
- Designed and maintained REST APIs serving 500,000+ daily requests
- Migrated legacy monolith to microservices, reducing latency by 40%
- Built an internal data pipeline using Python and PostgreSQL
- Mentored 2 junior engineers on code quality and Git workflow
 
Intern — TCS, Hyderabad (Jun 2021 – Dec 2021)
- Developed a dashboard for tracking CI/CD pipeline status using Django
- Wrote unit tests achieving 85% code coverage across the module
 
LANGUAGES
English (fluent), Hindi (native), Telugu (conversational)
"""
 
 
def analyze_resume(resume_text: str, job_role: str = "AI/ML Engineer") -> dict:
    """Send resume to OpenAI and return structured extraction."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,   # very low — we want consistent, factual extraction
        max_tokens=1000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Job role being evaluated for: {job_role}\n\nResume:\n{resume_text}"
            }
        ]
    )
    return json.loads(response.choices[0].message.content)
 
 
def print_report(data: dict) -> None:
    """Print a human-readable summary of the extracted data."""
    print("=" * 60)
    print("RESUME ANALYSIS REPORT")
    print("=" * 60)
    print(f"Name             : {data.get('name')}")
    print(f"Email            : {data.get('email')}")
    print(f"Phone            : {data.get('phone')}")
    print(f"Location         : {data.get('location')}")
    print(f"Experience       : {data.get('years_of_experience')} years")
    print(f"Suitability      : {data.get('suitability_score')}/10")
    print(f"Reason           : {data.get('suitability_reason')}")
    print()
    print("Summary:")
    print(f"  {data.get('summary')}")
    print()
    print("Skills:")
    print(f"  {', '.join(data.get('skills', []))}")
    print()
    print("Education:")
    for edu in data.get("education", []):
        print(f"  {edu['degree']} — {edu['institution']} ({edu.get('year', 'N/A')})")
    print()
    print("Experience:")
    for exp in data.get("experience", []):
        print(f"  {exp['title']} at {exp['company']} ({exp['duration']})")
        for h in exp.get("highlights", [])[:2]:
            print(f"    - {h}")
    print()
    print("Languages:")
    print(f"  {', '.join(data.get('languages', []))}")
    print()
    print("Raw JSON output:")
    print(json.dumps(data, indent=2))
 
 
if __name__ == "__main__":
    print("Analyzing resume...\n")
    result = analyze_resume(SAMPLE_RESUME, job_role="GenAI / LLM Engineer")
    print_report(result)
 

