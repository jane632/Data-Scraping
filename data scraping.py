from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Path to your ChromeDriver
path = r'C:\Users\hp\Downloads\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Open the website
driver.get('https://www.adamchoi.co.uk/overs/detailed')

wait = WebDriverWait(driver, 10)

# Wait for the season dropdown to be present and select the season
season_dropdown = wait.until(EC.presence_of_element_located((By.ID, "season")))
Select(season_dropdown).select_by_visible_text("2024/2025")

# Wait for the "All Matches" button to be clickable
all_matches_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//label[@analytics-event="All matches"]'))
)

# Remove the blocking ad iframe in a simple way
driver.execute_script("document.querySelector('iframe[id^=google_ads_iframe]')?.remove();")

# Scroll button into view (optional but helpful)
driver.execute_script("arguments[0].scrollIntoView();", all_matches_button)

# Click the "All Matches" button
all_matches_button.click()

# Wait for the page to update
time.sleep(5)

# Scrape the matches table
matches = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

date = []
home_team = []
score = []
away_team = []

for match in matches:
    try:
        date_text = match.find_element(By.XPATH, './td[1]').text
        home_text = match.find_element(By.XPATH, './td[3]').text
        score_text = match.find_element(By.XPATH, './td[4]').text
        away_text = match.find_element(By.XPATH, './td[5]').text

        date.append(date_text)
        home_team.append(home_text)
        score.append(score_text)
        away_team.append(away_text)

        #print(f"{date_text} | {home_text} vs {away_text} | Score: {score_text}")

    except Exception as e:
        print(f"Skipping a row due to error: {e}")

driver.quit()

# Save to CSV
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)

print(df)
