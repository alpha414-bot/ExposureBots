import logging
import os
import time
import traceback
from Account import VideoAccount as Accounts
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

logging.basicConfig(
    # filename="logs/main.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)

MAX_LIMIT = 12


class Check:
    def __init__(self, email, password, person) -> None:
        self.email = email
        self.password = password
        self.person = person
        self.driver = webdriver.Chrome(options=self.chrome_options())
        self.wait = WebDriverWait(self.driver, timeout=6)
        self.running = True
        self.vars = {}

    def start(self):
        try:
            self.driver.get(
                "https://paloaltou.co1.qualtrics.com/jfe/form/SV_3sZn2ag72SdTjE2",
                # "https://research.sc/participant/login/dynamic/42F0309D-859F-4A68-9207-5E952ADB85D8?external_id=0789abed-f21e-46d4-b4d9-45ca5389dafd&GUID=0789abed-f21e-46d4-b4d9-45ca5389dafd&Bypass=99&session=5&R1STATUS=0&R2STATUS=0&Confirm_id=58294137615"
            )
            self.main_section()
        except Exception as e:
            logging.error(f"Error during start for {self.email}: {e}")
            logging.error(traceback.format_exc())
            raise

    def teardown_method(self, message="Message is here"):
        """Teardown method to quit the WebDriver and show a message box."""
        logging.info(f"Finished process for {self.email}")
        logging.warning("Driver is quitting")
        self.running = False
        self.driver.quit()
        os.system(
            'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
            f"[System.Windows.Forms.MessageBox]::Show('{message}')\""
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
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--headless")  # Optional: run in headless mode
        # User Agent
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        # Media Video Controller
        chrome_options.add_argument(
            rf"--use-file-for-fake-video-capture=C:\Users\owner\Desktop\projects\bots\Exposure\{self.person.capitalize()}_Video.y4m"
        )
        return chrome_options

    def _visible_section(self, locator: str, timeout: float = 3):
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

            def I_Question():
                logging.info("<<< Question Section Thread >>>")
                while self.running:
                    try:
                        self.driver.execute_script(
                            f"document.title = '[{self.email}] Check Exposure ';"
                        )
                        if not self._visible_section("#Questions"):
                            self.teardown_method(
                                message=f"AVAILABLE: Research for [{self.email}] is available."
                            )
                            self.driver.quit()
                        else:
                            Text = self.driver.find_element(By.ID, "Questions").text
                            if (
                                ("You have completed" in Text)
                                or ("It has been less than" in Text)
                                or ("It appears there may be an error" in Text)
                                or ("your session has expired" in Text)
                            ):
                                # This email research is done
                                self.teardown_method(
                                    f"DONE: [{self.email}] research is done already."
                                )
                                self.driver.quit()
                                break
                            else:
                                self.teardown_method(
                                    message=f"AVAILABLE: Research for [{self.email}] is available."
                                )
                                self.driver.quit()

                    except:
                        continue

            I_Question()
        except:
            print(f"Traceback is ${traceback.format_exc()}")


def run_in_batches(emails_and_passwords: List[Tuple[str, str, str]]):
    total_accounts = len(emails_and_passwords)
    max_simultaneous = MAX_LIMIT if total_accounts >= MAX_LIMIT else total_accounts

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

    os.system(
        'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
        "[System.Windows.Forms.MessageBox]::Show('ALL PROCESSES ARE DONE. PLEASE CLOSE OR STOP TERMINAL NOW')\""
    )


def run_single_account(email: str, password: str, person: str):
    logging.info(f"Starting process for {email}")
    test = Check(email=email, password=password, person=person)
    try:
        test.start()
    finally:
        logging.info(f"Finished process for {email}")
        time.sleep(10)  # Introduce a delay to minimize CPU and network strain


if __name__ == "__main__":
    run_in_batches(Accounts())
