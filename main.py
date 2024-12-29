from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


PROMISED_DOWN = 600
PROMISED_UP = 400
TWITTER_EMAIL = "YOUR TWITTER EMAIL "
TWITTER_PASSWORD = "YOUR TWITTER PASSWORD"
TWITTER_USERNAME = "YOUR TWITTER USERNAME"


class InternetSpeedComplaintBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(name="detach", value=True)
        self.driver = webdriver.Chrome(options=chrome_options)


    def get_internet_speed(self) -> tuple:
        """Returns internet speed (down and up) in MB/s."""
        self.driver.get("https://www.speedtest.net")
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 60)

        # Allow cookies:
        time.sleep(1.5)
        allow_btn = self.driver.find_element(By.ID, value='onetrust-accept-btn-handler')
        allow_btn.click()

        # Click on Go to measure speed:
        time.sleep(1.5)
        go_btn = self.driver.find_element(By.CLASS_NAME, value='start-text')
        go_btn.click()

        back_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')))
        back_btn.click()


        # Extracting download and upload speeds:
        download_speed = float(self.driver.find_element(By.CLASS_NAME, value='download-speed').text)
        upload_speed = float(self.driver.find_element(By.CLASS_NAME, value='upload-speed').text)

        return download_speed, upload_speed


    def tweet(self, message):
        self.driver.get("https://twitter.com/")

        wait = WebDriverWait(self.driver, 60)


        time.sleep(3)
        accept_cookies = self.driver.find_element(By.XPATH, value='//*[text()="Accept all cookies"]')
        accept_cookies.click()


        time.sleep(4)
        sign_in_btn = self.driver.find_element(By.XPATH, value='//*[text()="Sign in"]')
        sign_in_btn.click()


        time.sleep(2)
        entry_1 = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label')
        entry_1.send_keys(TWITTER_EMAIL, Keys.ENTER)


        # Unusual activity bypass: - uncomment when it pops up.
        time.sleep(2)
        entry_2 = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        entry_2.send_keys(TWITTER_USERNAME, Keys.ENTER)

        time.sleep(2)
        entry_3 = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label')
        entry_3.send_keys(TWITTER_PASSWORD, Keys.ENTER)

        tweet = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))
        tweet.send_keys(message)

        time.sleep(2)
        tweet_button = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
        tweet_button.click()



bot = InternetSpeedComplaintBot()
download, upload = bot.get_internet_speed()

if download < PROMISED_DOWN - 50 or upload < PROMISED_UP - 50: # Subtracting 50 to allow for room
    message = f"Hey Internet Provider, why is my Internet speed {download}down/{upload}up when I pay for 600down/400up?"
else:
    message = f"Hey Internet Provider, my Internet speed is excellent today! Keep up the good work!"

bot.tweet(message)




