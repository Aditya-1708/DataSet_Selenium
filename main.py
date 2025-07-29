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

# Setup Chrome options
options = webdriver.ChromeOptions()
# Headless works now if stealth is used (still, test with it off first)
# options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1280,800")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Bypass bot detection
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)

# Go to the page
driver.get("https://www.naukri.com/nodejs-jobs?k=nodejs")

try:
    # Wait for job listings
    elem = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cust-job-tuple"))
    )

    file = 0
    print(f"\n✅ Found {len(elem)} job cards!")
    for ele in elem:
        d = ele.get_attribute("outerHTML")
        with open(f"data/naukri_{file}.html","w",encoding="utf-8") as f:
            f.write(d)
            file+=1
        # time.sleep(random(2,3))
    # for i, job in enumerate(job_cards[:21]):
    #     print(f"\nJob {i+1}:\n{job.text[:200]}...")

except Exception as e:
    print("❌ Error occurred:")
    traceback.print_exc()
    driver.save_screenshot("naukri_debug.png")  # debug image

finally:
    driver.quit()

