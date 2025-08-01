from bs4 import BeautifulSoup
import json
import os
import re

# Path to your HTML files
FOLDER_PATH = "./data"
OUTPUT_JSON = "grouped_jobs.json"

# Final structure: { "frontendengineer": [...], "backendengineer": [...] }
grouped_jobs = {}

# Loop through HTML files in the folder
for filename in os.listdir(FOLDER_PATH):
    if filename.lower().endswith(".html"):
        file_path = os.path.join(FOLDER_PATH, filename)
        print(f"📄 Processing {filename}")

        # Normalize the category: remove numbers, spaces, extension
        category = re.sub(r'[\s\d]+', '', filename.rsplit('.', 1)[0]).lower()

        # Ensure category exists
        if category not in grouped_jobs:
            grouped_jobs[category] = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml")
        except Exception as e:
            print(f"❌ Could not read {filename}: {e}")
            continue

        jobs = soup.find_all("div", class_="cust-job-tuple")

        for job in jobs:
            try:
                title_tag = job.find("a", class_="title")
                company_tag = job.find("a", class_="comp-name")
                rating_tag = job.find("a", class_="rating")
                review_tag = job.find("a", class_="review")
                exp_tag = job.find("span", class_="expwdth")
                loc_tag = job.find("span", class_="locWdth")
                desc_tag = job.find("span", class_="job-desc")
                tags = [li.get_text(strip=True) for li in job.select("ul.tags-gt li")]
                posted_tag = job.find("span", class_="job-post-day")
                logo_tag = job.find("img", class_="logoImage")

                job_data = {
                    "title": title_tag.get_text(strip=True) if title_tag else None,
                    "job_url": title_tag['href'] if title_tag else None,
                    "company": company_tag.get_text(strip=True) if company_tag else None,
                    "company_url": company_tag['href'] if company_tag else None,
                    "rating": rating_tag.get_text(strip=True) if rating_tag else None,
                    "reviews": review_tag.get_text(strip=True) if review_tag else None,
                    "experience": exp_tag.get_text(strip=True) if exp_tag else None,
                    "location": loc_tag.get_text(strip=True) if loc_tag else None,
                    "description": desc_tag.get_text(strip=True) if desc_tag else None,
                    "tags": tags,
                    "posted": posted_tag.get_text(strip=True) if posted_tag else None,
                    "logo": logo_tag['src'] if logo_tag else None,
                    "via":"Naukri.com"
                }

                grouped_jobs[category].append(job_data)

            except Exception as e:
                print(f"⚠️ Error parsing a job in {filename}: {e}")

# Write the grouped dictionary to JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(grouped_jobs, f, ensure_ascii=False, indent=2)

print(f"\n✅ DONE. Grouped jobs saved in: {OUTPUT_JSON}")
