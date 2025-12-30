from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from datetime import datetime

CHANNEL_URL = "https://www.youtube.com/@google/videos"
VIDEO_FILE = "last_video.txt"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get(CHANNEL_URL)

#  STEP 1: Handle cookie popup if exists
try:
    consent = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button//span[text()='Accept all']")
        )
    )
    consent.click()
except:
    pass

#  STEP 2: Scroll page (VERY IMPORTANT)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# STEP 3: Wait for video cards (robust locator)
latest_video = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a#video-title-link")
    )
)

latest_video_url = latest_video.get_attribute("href")
driver.quit()

#  Save & compare
if not os.path.exists(VIDEO_FILE):
    with open(VIDEO_FILE, "w") as f:
        f.write(latest_video_url)
    print(" Initial video saved.")
else:
    with open(VIDEO_FILE, "r") as f:
        old = f.read()

    if latest_video_url != old:
        print(" NEW VIDEO UPLOADED!")
        with open(VIDEO_FILE, "w") as f:
            f.write(latest_video_url)
    else:
        print(" No new video.")
