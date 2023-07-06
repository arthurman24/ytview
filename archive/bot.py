import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
import threading


def open_profile(profile_path, proxy, keyword, video_title, max_duration, next_profile_path):
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--mute-audio")
    options.add_argument('--disable-notifications')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(
        options=options,
        # seleniumwire_options={'proxy': proxy}
    )

    driver.set_window_size(1000, 800)

    try:
        # print("Opening Whoer ...")
        # # Go to the Google home page
        # driver.get('https://whoer.net/')

        print(f"Opened Chrome with Profile: {profile_path}")

        print("Opening Youtube ...")
        # Go to Youtube
        driver.get("https://www.youtube.com")

        # Wait split second for website to load
        time.sleep(5)

        # Find Search Bar Element
        print("Finding Searchbar ...")
        search_bar = WebDriverWait(driver, 360).until(EC.visibility_of_element_located((By.NAME, "search_query")))

        # Add keyword to the url
        driver.get(driver.current_url + "results?search_query=slot+gacor+hari+ini")

        # Wait split second for website to load
        time.sleep(5)

        # Wait until the search results are loaded
        print("Finding Content ...")
        WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, "content")))

        # Add filter for the last hour
        print("Applying Filter ...")
        driver.get(driver.current_url + "&sp=EgQIARAB")

        # Wait for the last hour to apply
        time.sleep(2)

        # Scroll to find the video
        print("Scrolling to find Video ...")
        found_video = scroll_to_find_video(driver, video_title)

        if found_video:
            # Click the video element
            print("Video Found. Clicking...")
            found_video.click()
        else:
            print("Video not found.")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error occurred while opening profile: {str(e)}")

    # Sleep for the specified duration
    time.sleep(5)

    # Open the next profile
    return next_profile_path


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


if __name__ == '__main__':

    keyword = "slot gacor"
    video_title = "slot gaor"
    max_duration = "450"
    folder_path = ""
    proxies = []
    profile_paths = []

    with open('proxies.txt', 'r') as file:
        for line in file:
            proxy = line.strip()
            proxies.append({'https': proxy})    

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isdir(file_path):
            profile_paths.append(file_path)

    # Create a thread for each profile
    threads = []
    for i in range(0, len(profile_paths), 5):
        for j in range(i, min(i + 5, len(profile_paths))):
            profile_path = profile_paths[j]
            proxy = proxies[j % len(proxies)]
            next_profile_path = profile_paths[(j + 1) % len(profile_paths)]

            thread = threading.Thread(target=open_profile, args=(profile_path, proxy, keyword, video_title, max_duration, next_profile_path))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Open another 5 tabs
        if i + 5 < len(profile_paths):
            input("Press Enter to exit...")
            time.sleep(5)  # Sleep for 5 seconds between opening batches of tabs


time.sleep(max_duration)
