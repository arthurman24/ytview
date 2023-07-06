from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
import signal
from colorama import init, Fore
import threading

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

def run_chrome(profile_path, urls, video_title):
    print(Fore.LIGHTYELLOW_EX + "Opening: " + profile_path)

    # Create ChromeOptions
    options = webdriver.ChromeOptions()

    # Specify the path to the Chrome profile directory
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Disable popup and welcome screen
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    # Disable the "Chrome is being controlled by automated test software" message
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)

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

def signal_handler(signal, frame):
    # Handle Ctrl + C and stop the threads
    for thread in chrome_threads:
        thread.stopped = True
    sys.exit(0)


if __name__ == '__main__':

    # Read video title from video.txt
    with open("urls.txt", "r", encoding="utf-8") as f:
        urls = f.read().strip()

    # Read keyword from keyword.txt
    with open("title.txt", "r", encoding="utf-8") as f:
        video_title = f.read().strip()

    # Specify the folder path where the profile directories are located
    get_folder = os.getcwd()
    folder_path = f"{get_folder}\\chromeprofile"

    # List of profile paths
    profile_paths = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]  

    # Create a list to hold the Chrome threads
    chrome_threads = []

    # Create and start Chrome threads for each profile
    for profile_path in profile_paths:
        thread = threading.Thread(target=run_chrome, args=(profile_path, urls, video_title))
        thread.stopped = False  # Custom attribute to track thread termination
        chrome_threads.append(thread)
        thread.start()

    # Register the signal handler for Ctrl + C
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for all Chrome threads to finish
    for thread in chrome_threads:
        thread.join()

time.sleep(max_watch)