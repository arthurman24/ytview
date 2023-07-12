import undetected_chromedriver as uc
import time
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

# Specify the folder path where the profile directories are located
get_folder = os.getcwd()
folder_path = f"{get_folder}\\chromeprofile"
max_watch = int(sys.argv[1])

# Read login credentials from a text file
credentials = []

with open("credentials.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        email, password = line.strip().split(",")
        credentials.append((email, password))

# Get the latest profile number
latest_profile_number = 0
for folder_name in os.listdir(folder_path):
    if folder_name.startswith("Profile"):
        profile_number = int(folder_name.split(" ")[1])
        latest_profile_number = max(latest_profile_number, profile_number)

# Create a new folder for each profile path
profile_paths = []
for i in range(len(credentials)):
    profile_number = latest_profile_number + i + 1
    profile_path = f"{folder_path}\\Profile {profile_number}"
    os.makedirs(profile_path, exist_ok=True)
    print(f"Created folder {profile_path}")
    profile_paths.append(profile_path)

# Create a list to store the Chrome drivers
drivers = []

# Iterate over profile paths and login credentials
for i, profile_path in enumerate(profile_paths):
    print(profile_path)

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Disable popup and welcome screen
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # use specific (older) version
    driver = uc.Chrome(
        options = options
    ) 

    driver.set_window_size(1000, 800)
    
    drivers.append(driver)

    try:
        driver.get("https://accounts.google.com/v3/signin/identifier?dsh=S-1727523073%3A1688684411243226&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AeDOFXgYyOctEzUEfaTCAzNeV4T1SDO-n11c-kzFyVlJocKCKMCTi1o_24B3lMIicHNGt6tRQARy&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

        # WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="openid-buttons"]/button[1]')))
        # button = driver.find_element(By.XPATH, '//*[@id="openid-buttons"]/button[1]')
        # button.click()

        email, password = credentials[i % len(credentials)]

        email_field = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.ID, "identifierId"))
        )

        email_field = driver.find_element(By.ID, "identifierId")
        email_field.send_keys(email)

        # Click the Next button
        next_button = driver.find_element(By.ID, "identifierNext")
        next_button.click()

        # Wait for the password input field to be visible
        password_field = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password'][name='password'], input[type='password'][name='Passwd']"))
        )

        # Enter your password
        password_field.send_keys(password)

        # Click the Next button
        next_button = driver.find_element(By.ID, "passwordNext")
        next_button.click()

        time.sleep(5)

    except Exception as e:
        print(f"Error occurred while opening Chrome with Error: {str(e)}")    
        
time.sleep(60 * max_watch)