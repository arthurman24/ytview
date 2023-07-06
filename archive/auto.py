import undetected_chromedriver as uc
import time
import os
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from colorama import init, Fore

init(autoreset=True)

def scroll_to_find_video(driver, video_title):
    scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
    current_height = 0

    while current_height < scroll_height:
        current_height += 500  # Scroll down by 500 pixels
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(2)  # Wait for page to settle after scrolling

        try:
            video_element = driver.find_element(By.XPATH, f"//a[contains(@title, '{video_title}')]")
            return video_element
        except NoSuchElementException:
            continue

    return None

def run_profile(profile_directory, urls, video_title, max_watch):
    options = uc.ChromeOptions()

    # setting profile
    options.add_argument(f"--user-data-dir={profile_directory}")
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
        suppress_welcome=False,
        options = options
    ) 

    driver.set_window_size(1000, 800)

    try:
        print(Fore.LIGHTYELLOW_EX + "Opening Youtube ...")
        # Go to Youtube
        driver.get("https://www.whoer.net")
        driver.get("https://www.youtube.com")

        # Find Search Bar Element
        print(Fore.LIGHTYELLOW_EX + "Finding Searchbar ...")
        search_bar = WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.NAME, "search_query")))

        time.sleep(5)

        # Add keyword to the url
        driver.get(driver.current_url + urls)

        # Wait for the page to load completely
        print(Fore.LIGHTYELLOW_EX + "Waiting for the page to load ...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@title, 'YouTube')]")))

        # Scroll to find the video
        print(Fore.LIGHTYELLOW_EX + "Scrolling to find Video ...")
        found_video = scroll_to_find_video(driver, video_title)   

        if found_video:
            # Click the video element
            print(Fore.LIGHTYELLOW_EX + "Video Found. Clicking...")
            found_video.click()
        else:
            print(Fore.LIGHTYELLOW_EX + "Video not found.")

    except (TimeoutException, NoSuchElementException) as e:
        print(Fore.LIGHTYELLOW_EX + f"Error occurred while opening profile: {str(e)}")

# Auto Views Youtube 0.1.0
print(Fore.LIGHTGREEN_EX + "+-------------------------- Version: 0.1.0 --------------------------+")

# Get max_watch from user
max_watch = input(Fore.LIGHTBLUE_EX + "Enter the maximum watch time in minutes (default: 5): ")
if not max_watch:
    max_watch = 5
else:
    max_watch = int(max_watch)

# Read video title from video.txt
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = f.read().strip()

# Read keyword from keyword.txt
with open("title.txt", "r", encoding="utf-8") as f:
    video_title = f.read().strip()

# Specify the folder path where the profile directories are located
folder_path = "C:\\Users\\BLUE I.T COMPUTER\\Documents\\seo\\python tools\\chromeprofile"

# Retrieve profile directories from the folder path
profile_directories = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

for i in range (len(profile_directories)):
    run_profile(profile_directories[i], urls, video_title, max_watch)

time.sleep(60 * max_watch)
print(Fore.LIGHTGREEN_EX + "+-------------------------- Script completed --------------------------+")