import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os

# Set folder path where u want to put ur profile
folder_path = "C:\\Users\\BLUE I.T COMPUTER\\Documents\\seo\\python tools\\chromeprofile"

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

# Iterate over profile paths and login credentials
for i, profile_path in enumerate(profile_paths):
    print(f"Logging in with Profile {i+1}")

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--mute-audio")
    options.add_argument('--disable-notifications')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # use specific (older) version
    driver = uc.Chrome(
    suppress_welcome=False,
    options = options , version_main = 94
    )  # version_main allows to specify your chrome version instead of following chrome global version

    driver.set_window_size(1000, 800)

    try:
        # Perform actions in the Chrome instance
        # ...
        driver.get("https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent")

        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="openid-buttons"]/button[1]')))

        button = driver.find_element(By.XPATH, '//*[@id="openid-buttons"]/button[1]')

        button.click()

        email, password = credentials[i % len(credentials)]  # Wrap around the credentials list

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

        time.sleep(20)

        # Now you should be logged in and can perform further actions
        driver.get('https://www.google.com/')

    except Exception as e:
        print(f"Error occurred while opening Chrome with Error: {str(e)}")    
    
time.sleep(120)
