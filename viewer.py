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
max_watch = int(sys.argv[1])

def scroll_to_find_video(driver, video_title):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        try:
            video_element = driver.find_element(By.XPATH, f"//a[contains(@title, '{video_title}')]")
            return video_element
        except NoSuchElementException:
            pass

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return None

def run_profile(profile_directory, urls, video_title, max_watch):
    print(Fore.LIGHTYELLOW_EX + "Opening: " + profile_directory)

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
        driver.get(urls)

        time.sleep(5)

        # Wait for the page to load completely
        print(Fore.LIGHTYELLOW_EX + "Waiting for the page to load ...")
        WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@title, 'YouTube')]")))

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

    return driver

# Read video title from video.txt
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = f.read().strip()

# Read keyword from keyword.txt
with open("title.txt", "r", encoding="utf-8") as f:
    video_title = f.read().strip()

# Specify the folder path where the profile directories are located
folder_path = "C:\\Users\\BLUE I.T COMPUTER\\Documents\\seo\\youtubeview\\chromeprofile"

# Retrieve profile directories from the folder path
profile_directories = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

drivers = []

for i in range(min(len(profile_directories), 30)):
    driver = run_profile(profile_directories[i], urls, video_title, max_watch)
    drivers.append(driver)

time.sleep(60 * max_watch)
print(Fore.LIGHTGREEN_EX + "+-------------------------- Script completed --------------------------+")