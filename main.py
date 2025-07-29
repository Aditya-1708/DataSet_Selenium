from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
import random
import traceback
import json

# Load the JSON file
with open("jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

options = webdriver.ChromeOptions()
# Headless works now if stealth is used (still, test with it off first)
# options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1280,800")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)
for section in data:
    print(f"📂 Category: {section['category']}")
    for title in section["titles"]:
# Go to the page
            for page in range(1, 50):
                url = f"https://www.naukri.com/{title}-jobs-{page}"
                driver.get(url)

                try:
                    elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cust-job-tuple"))
                    )

                    if not elem:
                        print(f"🚫 No jobs found on page {page}, stopping.")
                        break

                    file = 0
                    print(f"\n✅ Found {len(elem)} job cards on page {page}!")
                    for ele in elem:
                        d = ele.get_attribute("outerHTML")
                        with open(f"data/{title}_{page}_{file}.html", "w", encoding="utf-8") as f:
                            f.write(d)
                        file += 1
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ Error on page {page} for title '{title}':")
                    traceback.print_exc()
                    driver.save_screenshot(f"naukri_debug_{title}_{page}.png")
                    break  # stop further page scraping for this title if error occurs

driver.quit()