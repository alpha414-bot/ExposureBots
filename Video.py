import logging
import os
import time
import traceback
from typing import List, Tuple
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.action_chains import ActionChains
import threading
import urllib3

logging.basicConfig(
    # filename="logs/main.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)


class Video:
    def __init__(self, email, password, person) -> None:
        logging.info("```<< started class >>```")
        self.email = email
        self.password = password
        self.person = person
        self.driver = webdriver.Chrome(options=self.chrome_options())
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.vars = {}
        self.running = True

    def start(self):
        try:
            self.driver.get(
                # "https://paloaltou.co1.qualtrics.com/jfe/form/SV_3sZn2ag72SdTjE2",
                "https://research.sc/participant/login/dynamic/42F0309D-859F-4A68-9207-5E952ADB85D8?external_id=0789abed-f21e-46d4-b4d9-45ca5389dafd&GUID=0789abed-f21e-46d4-b4d9-45ca5389dafd&Bypass=99&session=5&R1STATUS=0&R2STATUS=0&Confirm_id=58294137615"
            )
            self.main_section()
        except Exception as e:
            logging.error(f"Error during start for {self.email}: {e}")
            logging.error(traceback.format_exc())
            raise

    def teardown_method(self):
        """Teardown method to quit the WebDriver and show a message box."""
        logging.info(f"Finished process for {self.email}")
        logging.warning("Driver is quitting")
        self.driver.quit()
        os.system(
            'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
            f"[System.Windows.Forms.MessageBox]::Show('Your research for [{self.email}] is done.')\""
        )

    def chrome_options(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # Media
        prefs = {
            "profile.default_content_setting_values.media_stream_mic": 1,  # Allow microphone
            "profile.default_content_setting_values.media_stream_camera": 1,  # Allow camera
            "profile.default_content_setting_values.geolocation": 1,  # Allow geolocation
            "profile.default_content_setting_values.notifications": 1,  # Allow notifications
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_argument("--use-fake-device-for-media-stream")
        chrome_options.add_argument("--auto-accept-camera-and-microphone-capture")
        chrome_options.add_argument("--disable-infobars")
        user_data_dir = r"C:\Users\owner\AppData\Local\Google\Chrome\User Data"
        profile_directory = (
            r"C:\Users\owner\AppData\Local\Google\Chrome\User Data\Profile 2"
        )
        # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        # chrome_options.add_argument(f"--profile-directory={profile_directory}")
        # User Agent
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        # Media Video Controller
        if self.person.lower() == "alpha":
            chrome_options.add_argument(
                r"--use-file-for-fake-video-capture=C:\Users\owner\Desktop\projects\bots\Alpha_Video.y4m"
            )
        elif self.person.lower() == "femi":
            chrome_options.add_argument(
                r"--use-file-for-fake-video-capture=C:\Users\owner\Desktop\projects\bots\Femi_Video.y4m"
            )
        return chrome_options

    def _check_section(self, locator: str):
        """Checks if a section is present by the specified locator."""
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
        except:
            return False

    def _visible_section(self, locator: str, timeout: float = 4):
        """Checks if a section is visible by the specified locator."""
        try:
            custom_wait = WebDriverWait(self.driver, timeout=timeout)
            return custom_wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator))
            )
        except:
            return False

    def _enter_text(self, locator: str, value: str | int):
        """Enters text into an input field located by the specified locator."""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.send_keys(value)  # type: ignore
            logging.info(f"<< {locator} new value [{value}] is entered >>> ")
            return True
        except:
            return False

    def _click_button(self, locator: Tuple[str, str] = (By.ID, "NextButton")):
        """Clicks a button located by the specified locator."""
        try:
            button = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            self.driver.execute_script("arguments[0].click();", button)
            logging.info(f"... {locator} button is clicked for [{self.email}] ...")
            self.driver.implicitly_wait(1)
            return True
        except:
            return False

    def main_section(self):
        # Login
        logging.info("``` main section ```")
        try:
            """Performs login using the provided email and password."""
            if self._visible_section("input[name='QR~Authentication-FL_95~0~TEXT']"):
                self._enter_text(
                    "input[name='QR~Authentication-FL_95~0~TEXT']", self.email
                )
            if self._visible_section("input[name='QR~Authentication-FL_95~1~TEXT']"):
                self._enter_text(
                    "input[name='QR~Authentication-FL_95~1~TEXT']", self.password
                )
        finally:
            self._click_button()  # login to account
            self.index_section()

    def index_section(self):
        try:
            logging.info("`` touch here ``")

            def I_Question():
                logging.info("<<< Question Section Thread >>>")
                while self.running:
                    try:
                        if self._visible_section("#Questions"):
                            Text = self.driver.find_element(By.ID, "Questions").text
                            if "You can download the handout" in Text:
                                if self._check_section("#NextButton"):
                                    self._click_button()
                            if "you will be asked to watch" in Text:
                                if self._check_section("#NextButton"):
                                    self._click_button()
                            # Add a condition to break out of the loop when the task is done
                            if (
                                ("You have completed" in Text)
                                or ("It has been less than" in Text)
                                or ("It appears there may be an error" in Text)
                            ):
                                logging.info("Done ... Text")
                                self.running = False  # stop runing the loop, video is done completely
                                self._click_button()
                                break
                    except:
                        continue

            def I_Gorilla():
                logging.info("<<< Gorilla Section Thread >>>")
                while self.running:
                    try:
                        if self._visible_section("#gorilla", timeout=0.2):
                            parent_elements = self.wait.until(
                                EC.visibility_of_any_elements_located(
                                    (By.CSS_SELECTOR, "#gorilla div.lookahead-frame")
                                )
                            )
                            for look_element in parent_elements:
                                if look_element.is_displayed():
                                    try:
                                        continue_button = look_element.find_element(
                                            By.ID, "continue-button"
                                        )
                                        continue_button.click()
                                    except:
                                        continue
                    except:
                        continue

            def I_SliderRange():
                logging.info("<<< slider range Thread >>>")
                while self.running:
                    try:
                        parent = self._visible_section(".gorilla-content-slider.slider")
                        if parent:
                            print("Found a slider parent")
                            parent_element = parent.find_element(
                                By.CSS_SELECTOR, ".slider-track"
                            )
                            if parent_element:
                                print("Found a slider track")
                                slider_thumb = parent_element.find_element(
                                    By.CSS_SELECTOR, ".slider-handle"
                                )
                                if slider_thumb:
                                    print("Find a slider thumb")
                                    random_range_value = random.choice(
                                        range(35, 90)
                                    )  # The value you want to set
                                    random_range_value = random_range_value - 10
                                    offset = int(
                                        (random_range_value / 100)
                                        * parent_element.size["width"]
                                    )
                                    actions = ActionChains(self.driver)
                                    actions.click_and_hold(slider_thumb).move_by_offset(
                                        offset, 0
                                    ).release().perform()
                                    print(
                                        f"Slided me {offset}, percentage: {random_range_value}% "
                                    )
                                    self._click_button((By.ID, "continue-button"))
                        elif self._visible_section("#continue-button", timeout=0.2):
                            self._click_button((By.ID, "continue-button"))
                    except:
                        continue

            def I_ButtonSetup(id_locator):
                logging.info(f"<<< running button thread: {id_locator} >>>")
                while self.running:
                    self.driver.execute_script(
                        f"document.title = '[{self.email}] Video Exposure ';"
                    )
                    try:
                        if not self._visible_section(
                            "#Questions", timeout=0.2
                        ) or not self._visible_section("#gorilla", timeout=0.2):
                            if self._visible_section(f"#{id_locator}", timeout=0.2):
                                self._click_button((By.ID, f"{id_locator}"))
                    except:
                        continue

            I_QuestionThread = threading.Thread(target=I_Question)
            I_GorillaThread = threading.Thread(target=I_Gorilla)
            I_SliderRangeThread = threading.Thread(target=I_SliderRange)
            NextButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("NextButton",)
            )
            ContinueButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("continue-button",)
            )
            StartButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("start-button",)
            )
            MediaAccessButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("media-access-check",)
            )
            logging.info("... starting thread ...")
            I_QuestionThread.start()
            I_GorillaThread.start()
            I_SliderRangeThread.start()
            NextButtonThread.start()
            ContinueButtonThread.start()
            StartButtonThread.start()
            MediaAccessButtonThread.start()
            logging.info("... joining thread ...")
            I_QuestionThread.join()
            I_GorillaThread.join()
            I_SliderRangeThread.join()
            NextButtonThread.join()
            ContinueButtonThread.join()
            StartButtonThread.join()
            MediaAccessButtonThread.join()
        except:
            print(f"Traceback is ${traceback.format_exc()}")


def run_in_batches(emails_and_passwords: List[Tuple[str, str, str]]):
    total_accounts = len(emails_and_passwords)
    max_simultaneous = 4 if total_accounts > 4 else total_accounts

    logging.info(
        f"Running for {total_accounts} accounts, max simultaneous: {max_simultaneous}"
    )
    logging.info(
        f"Running for {total_accounts} accounts, max simultaneous: {max_simultaneous}"
    )

    # Loop through accounts in batches of `max_simultaneous`
    for i in range(0, total_accounts, max_simultaneous):
        batch = emails_and_passwords[i : i + max_simultaneous]
        logging.info(
            f"Running batch {i // max_simultaneous + 1} with {len(batch)} accounts"
        )

        with ThreadPoolExecutor(max_workers=max_simultaneous) as executor:
            futures = [
                executor.submit(run_single_account, email, password, person)
                for email, password, person in batch
            ]

            # Wait for all tasks in the batch to finish before starting the next batch
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    logging.error(f"An error occurred: {exc} {traceback.format_exc()}")

        logging.info(f"Batch {i // max_simultaneous + 1} finished")


def run_single_account(email: str, password: str, person: str):
    logging.info(f"Starting process for {email}")
    test = Video(email=email, password=password, person=person)
    try:
        test.start()
    finally:
        test.teardown_method()
        logging.info(f"Finished process for {email}")
        time.sleep(10)  # Introduce a delay to minimize CPU and network strain


if __name__ == "__main__":
    accounts = [
        ## Alpha
        # ...
        # ("graychristian423@gmail.com", "247695Femi", "femi"),  # 10/09 20:22
        # ("jewelsabby2@gmail.com", "2585abigael", "femi"),  # 10/09 18:40
        # ("Deborahkate44@gmail.com", "2585abigael", "femi"),  # 10/09 20:23
        # ...
        # ("my.smtp000@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 20:24
        # ("adigunmiracle14@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 21:42
        # ("adigunmiracle41@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 21:41
        # ("moadigun30@student.lautech.edu.ng", "$Ola76lekan59", "alpha"), 🔥
        # ("adigungrace14@gmail.com", "$Ola76lekan59", "alpha"), 🔥
        # ("olayioyebukunmi@gmail.com", "$Ola76lekan59", "alpha"), 🔥
        # ...
        # ("lucasria.code@gmail.com", "$Ola76lekan59", "alpha"), # 10/09 15:46
        # ("olayioyetifebright@gmail.com", "$Ola76lekan59", "alpha"), # 10/09 15:37
        # ("undertestmiracle14@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 21:29
        ("noreplyhealthcarology@gmail.com", "$Ola76lekan59", "alpha"),  #
        # ("anabellac671@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 21:45
        # ("emmanueldav606@gmail.com", "$Pamilerin2006", "alpha"),
        # ("dev.butterfly202@gmail.com", "$Ola76lekan59", "alpha"),  # 10/09 22:31
        #
        # Post intervention done (wait list for 1 months)
        # ("alphasoft2021@gmail.com", "$Ola76lekan59", "alpha"), # 09/10
        # ("micheallukas08@gmail.com", "247695Femi", "femi"), # 09/10
    ]
    run_in_batches(accounts)
