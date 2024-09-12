from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import logging
from datetime import datetime, timedelta
import re
import random
import traceback
from typing import Tuple
import uuid
import time
import asyncio
from faker import Faker
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.file_manager import FileManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import OperationSystemManager
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(
    # filename="logs/main.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)


class Qualification:
    def __init__(self, email: str, password: str, person: str):
        fake = Faker()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.email = email
        self.password = password
        self.person = person
        self.uuid = str(uuid.uuid4())  # external_uuid and guid
        self.city = random.choice(
            ["New York", "California", "Texas", "illinois", "Washington"]
        )

    def teardown_method(self):
        """Teardown method to quit the WebDriver and show a message box."""
        logging.info(f"Finished process for {self.email}")
        logging.warning("Driver is quitting")
        # self.driver.quit()
        os.system(
            'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
            f"[System.Windows.Forms.MessageBox]::Show('Your research for [{self.email}] is done.')\""
        )

    def embbed_uid(self):
        return self.driver.execute_script(
            f"""
                    var d = new Date();
                    var fu1date = new Date(d.getTime() + 7 * 86400000);

                    var consentdate =
                    d.getUTCFullYear() +
                    "-" +
                    ("0" + (d.getUTCMonth() + 1)).slice(-2) +
                    "-" +
                    ("0" + d.getUTCDate()).slice(-2) +
                    " " +
                    ("0" + d.getUTCHours()).slice(-2) +
                    ":" +
                    ("0" + d.getUTCMinutes()).slice(-2) +
                    ":" +
                    ("0" + d.getUTCSeconds()).slice(-2);

                    Qualtrics.SurveyEngine.setEmbeddedData("CONSENTDATE", consentdate);
                    Qualtrics.SurveyEngine.setEmbeddedData("GUID", "{self.uuid}");
                    Qualtrics.SurveyEngine.setEmbeddedData("FU1DATE", fu1date);
        """,
        )

    def setup_method(self):
        chrome_options = Options()
        prefs = {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        user_data_dir = r"C:\Users\owner\AppData\Local\Google\Chrome\User Data"
        # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        # chrome_options.add_argument(r"--profile-directory='Profile 2'")
        chrome_options.add_argument("--use-fake-device-for-media-stream")
        chrome_options.add_argument("--auto-accept-camera-and-microphone-capture")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument(
            "--no-sandbox"
        )  # Sandbox issues sometimes cause crashes
        chrome_options.add_argument("--disable-dev-shm-usage")
        # gpu acceleration related
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
        chrome_options.add_argument(
            "--disable-software-rasterizer"
        )  # Disable SwiftShader fallback
        chrome_options.add_argument("--disable-gpu-process-early-init")
        chrome_options.add_argument("--disable-gpu-watchdog")
        chrome_options.add_argument("--disable-gpu-process-crash-limit")
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--headless")  # Optional: run in headless mode
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # protect from bot discovery
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        # Disable WebDriver property
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            rf"--use-file-for-fake-video-capture=C:\Users\owner\Desktop\projects\bots\Exposure\{self.person.capitalize()}_Video.y4m"
        )
        chrome_options.add_argument(
            r"--use-file-for-fake-audio-capture=C:\Users\owner\Desktop\projects\bots\audio.wav"
        )
        # Preventing error
        chrome_options.add_argument("--use-gl=egl")
        chrome_options.add_argument("--disable-vulkan")

        ###
        chrome_service = ChromeService(
            r"C:\drivers\chromedriver\chromedriver.exe"
        )  # Provide the path to chromedriver
        cache_manager = DriverCacheManager(
            file_manager=FileManager(os_system_manager=OperationSystemManager())
        )
        manager = ChromeDriverManager(cache_manager=cache_manager)
        os_manager = OperationSystemManager(os_type="win64")
        # self.driver = webdriver.Chrome(
        #     service=ChromeService(ChromeDriverManager().install()),
        #     options=chrome_options,
        # )
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.running = True
        self.age = random.choice(range(22, 26))
        self._dob()
        self.vars = {}

    def start(self):
        self.driver.get(
            "https://paloaltou.co1.qualtrics.com/jfe/form/SV_3sZn2ag72SdTjE2?Bypass=2&Gorilla=0"
        )
        logging.info(f"<<< External UID and GUID is {self.uuid} >>>")
        self.main_section()

    def _dob(self):
        try:
            current_date = datetime.now()
            birth_year = current_date.year - self.age
            # Step 4: Randomly select a month and day, ensuring the date is valid
            random_month = random.choice(range(1, 13))
            # Choose a day between 1 and the last day of the randomly chosen month
            if random_month == 2:  # February
                random_day = random.choice(
                    range(1, 29)
                )  # Assuming no leap year for simplicity
            elif random_month in [
                4,
                6,
                9,
                11,
            ]:  # April, June, September, November have 30 days
                random_day = random.choice(range(1, 31))
            else:  # All other months have 31 days
                random_day = random.choice(range(1, 32))

            # Step 5: Combine the year, month, and day to form a date
            random_dob = datetime(birth_year, random_month, random_day)

            # Step 6: Format the date in "mm/dd/yyyy" format
            formatted_dob = random_dob.strftime("%m/%d/%Y")
            self.date_of_birth = formatted_dob
            return formatted_dob
        except:
            return "02/13/2000"

    def _enter_text(self, locator: str, value: str | int, clickable: bool = False):
        try:
            match = re.search(r"QID\d+", locator)
            if match:
                parent_locator = match.group()  # type: ignore
                parent_locator = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, f".{parent_locator}")
                    )
                )
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, locator))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", element
                )
                element.send_keys(value)  # type: ignore
                if clickable:
                    self._click_button()
                logging.info(f"<< {locator} new value [{value}] is entered >>> ")
                return True
            else:
                logging.warning("!!! Unable to extract parent name !!!")
        except:
            return False

    def _click_label(self, locator: str, clickable: bool = False):
        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)
            if clickable:
                self._click_button()
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
            return True
        except:
            return False

    def _check_section(self, locator: str, timeout: float = 0.2):
        """Checks if a section is present by the specified locator."""
        try:
            custom_wait = WebDriverWait(self.driver, timeout=timeout)
            return custom_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
        except:
            return False

    def _visible_section(self, locator: str, timeout: float = 10):
        """Checks if a section is visible by the specified locator."""
        try:
            custom_wait = WebDriverWait(self.driver, timeout=timeout)
            return custom_wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator))
            )
        except Exception as e:
            return False

    def main_section(self):
        try:
            if self.wait.until(
                lambda driver: driver.execute_script(
                    "return Qualtrics.SurveyEngine.getEmbeddedData('GUID') !== null"
                )
            ):
                self.embbed_uid()
            else:
                self.embbed_uid()

            self.driver.execute_script(
                f"document.title = '[{self.email}] Qualification Exposure'; console.log('Personal Info', 'Name: {self.last_name} {self.first_name}')"
            )
            # agree to volunter
            self._click_label("label[for='QR~QID650~1']#QID650-1-label", True)
            # To complete the computerized task you MUST be on a computer with a webcamera and audio recording capability. (YES)
            self._click_label("label[for='QR~QID666~1']#QID666-1-label", True)

            # Personal info (age, sex, ethnicity, race, education level, city)
            self._enter_text("input[name='QR~QID652~TEXT']", self.age)
            self._click_label("label[for='QR~QID653~1']#QID653-1-label")
            self._click_label("label[for='QR~QID654~2']#QID654-2-label")
            self._click_label("label[for='QR~QID655~5']#QID655-5-label")
            self._click_label("label[for='QR~QID657~9']#QID657-9-label")
            self._enter_text("input[name='QR~QID779~TEXT']", self.city, True)

            # Language
            self._click_label("label[for='QR~QID658~1']#QID658-1-label", True)
            self._click_label("label[for='QR~QID660~2']#QID660-2-label", True)
            self._click_label("label[for='QR~QID664~2']#QID664-2-label", True)
            self._click_label("label[for='QR~QID677~1']#QID677-1-label")
            self._click_label("label[for='QR~QID678~1']#QID678-1-label", True)

            # smoking alchol and others section
            self._click_label("label[for='QR~QID683~2']#QID683-2-label")
            self._click_label("label[for='QR~QID750~1']#QID750-1-label")
            self._click_label("label[for='QR~QID751~7']#QID751-7-label")
            self._click_label("label[for='QR~QID752~1']#QID752-1-label", True)

            # all no answers
            self._click_label("label[for='QR~QID753~1~1']")
            self._click_label("label[for='QR~QID753~2~1']")
            self._click_label("label[for='QR~QID753~3~1']")
            self._click_label("label[for='QR~QID753~4~1']")
            self._click_label("label[for='QR~QID753~5~1']")
            self._click_label("label[for='QR~QID753~6~1']")
            self._click_label("label[for='QR~QID753~7~1']")
            self._click_label("label[for='QR~QID753~8~1']")
            self._click_label("label[for='QR~QID753~9~1']")
            self._click_label("label[for='QR~QID753~10~1']", True)

            # Taking prescribed medications
            self._click_label("label[for='QR~QID684~2']#QID684-2-label", True)

            # Diagnosed health medications
            self._click_label("label[for='QR~QID689~1~5']")
            self._click_label("label[for='QR~QID689~4~5']")
            self._click_label("label[for='QR~QID689~5~1']")
            self._click_label("label[for='QR~QID689~6~5']")
            self._click_label("label[for='QR~QID689~7~5']")
            self._click_label("label[for='QR~QID689~8~5']")
            self._click_label("label[for='QR~QID689~9~5']")
            self._click_label("label[for='QR~QID689~10~1']")
            self._click_label("label[for='QR~QID689~12~5']", True)

            # Fear and Anxiety avoidance scale
            options = ["3", "4"]
            for i in range(1, 25):
                self._click_label(
                    f"label[for='QR~QID781#1~{i}~{random.choice(options)}']"
                )
                self._click_label(
                    f"label[for='QR~QID781#2~{i}~{random.choice(options)}']"
                )
            self._click_button()

            # Problem bothering
            first_options = ["1", "2"]
            options = ["3", "4"]
            self._click_label(f"label[for='QR~QID755~22~{random.choice(options)}']")
            exclude = {17}
            for i in range(1, 21):
                if i not in exclude:
                    self._click_label(
                        f"label[for='QR~QID755~{i}~{random.choice(options)}']"
                    )
            self._click_label(
                f"label[for='QR~QID755~21~{random.choice(first_options)}']"
            )
            self._click_label(f"label[for='QR~QID755~23~1']")
            self._click_label(f"label[for='QR~QID755~24~1']", True)

            # problem bothering 2
            options = ["2", "3", "4"]
            for i in range(1, 10):
                self._click_label(
                    f"label[for='QR~QID761~{i}~{random.choice(options)}']"
                )
            self._click_button()

            # problem bothering 3
            options = ["3", "4"]
            for i in range(1, 8):
                self._click_label(
                    f"label[for='QR~QID762~{i}~{random.choice(options)}']"
                )
            self._click_button()

            # Health and mental conditions
            options = ["2", "3", "4"]
            exclude = {2, 33, 34}
            for i in range(1, 40):
                if i not in exclude:
                    self._click_label(
                        f"label[for='QR~QID763~{i}~{random.choice(options)}']"
                    )
            self._click_button()

            # Feeeling & Behaviours
            options = ["2", "3", "4"]
            exclude = {3, 4, 5}
            for i in range(1, 24):
                if i not in exclude:
                    self._click_label(
                        f"label[for='QR~QID775~{i}~{random.choice(options)}']"
                    )
            self._click_button()

            # Final Feeling & Communication with others
            self._click_label(f"label[for='QR~QID783~1~2']")
            self._click_label(f"label[for='QR~QID783~2~2']")
            self._click_label(f"label[for='QR~QID783~3~4']")
            self._click_label(f"label[for='QR~QID783~4~4']")
            self._click_label(f"label[for='QR~QID783~5~2']")
            self._click_label(f"label[for='QR~QID783~6~3']")
            self._click_label(f"label[for='QR~QID783~7~4']")
            self._click_label(f"label[for='QR~QID783~8~2']")
            self._click_label(f"label[for='QR~QID783~9~3']")
            self._click_label(f"label[for='QR~QID783~10~3']")
            self._click_label(f"label[for='QR~QID783~11~2']")
            self._click_label(f"label[for='QR~QID783~12~4']")
            self._click_label(f"label[for='QR~QID783~12~4']")
            self._click_label(f"label[for='QR~QID783~13~2']")
            self._click_label(f"label[for='QR~QID783~14~2']")
            self._click_label(f"label[for='QR~QID783~15~4']")
            self._click_label(f"label[for='QR~QID783~16~4']")
            self._click_label(f"label[for='QR~QID783~17~2']")
            self._click_label(f"label[for='QR~QID783~18~2']")
            self._click_label(f"label[for='QR~QID783~19~2']")
            self._click_label(f"label[for='QR~QID783~20~4']")
            self._click_label(f"label[for='QR~QID783~21~2']")
            self._click_label(f"label[for='QR~QID783~22~4']")
            self._click_label(f"label[for='QR~QID783~23~2']")
            self._click_label(f"label[for='QR~QID783~24~4']", True)

            # suicide notice
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f".QID785"))
            )
            self._click_button()

            # you are fit
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f".QID690"))
            )
            self._click_button()
            self.start_teleconferencing()
        except Exception as e:
            logging.error(
                f"Problem with main section for <<<[[[{self.email}]]]>>>: {traceback.format_exc()}"
            )
        finally:
            self._click_button()
            self.start_teleconferencing()

    # teleconferencing
    def start_teleconferencing(self):
        try:
            logging.info(
                f"<<< Teleconfering on qualifications beginning on {self.driver.current_url} >>>"
            )

            def I_Question():
                logging.info("<<< Question Section Thread >>>")
                while self.running:
                    try:
                        if self._visible_section("#Questions"):
                            Text = self.driver.find_element(By.ID, "Questions").text
                            if "You can download the handout" in Text:
                                if self._check_section("#NextButton", timeout=1):
                                    self._click_button()
                            # Add a condition to break out of the loop when the task is done
                            if "You have completed" in Text:
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
                            CustomWebWait = WebDriverWait(self.driver, timeout=0.2)
                            parent_elements = CustomWebWait.until(
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
                                    self.driver.implicitly_wait(5)
                                    self._click_button((By.ID, "continue-button"))
                        elif self._visible_section("#continue-button", timeout=0.2):
                            self._click_button((By.ID, "continue-button"))
                    except:
                        continue

            def I_ButtonSetup(id_locator):
                logging.info(f"<<< running button thread: {id_locator} >>>")
                while self.running:
                    self.driver.execute_script(
                        f"""
                        document.title = '[{self.email}] Qualification Exposure';
                        console.log(JSON.stringify({{
                            'uuid': '{self.uuid}',
                            'first_name': '{self.first_name}', 
                            'last_name': '{self.last_name}', 
                            'email': '{self.email}',
                            'city': '{self.city}',
                            'age': '{self.age}', 
                            'dob': '{self.date_of_birth}',
                        }}));
                        """
                    )
                    try:
                        if not self._visible_section(
                            "label"
                        ) and not self._visible_section("input"):
                            if not self._visible_section(
                                "#Questions", timeout=0.2
                            ) or not self._visible_section("#gorilla", timeout=0.2):
                                if self._visible_section(f"#{id_locator}", timeout=0.2):
                                    self._click_button((By.ID, f"{id_locator}"))
                    except:
                        continue

            def I_InstructionVideo():
                logging.info(
                    "<<< skipping instruction video and clicking on the title to skip"
                )
                while self.running:
                    try:
                        if self._visible_section(
                            "h1.gorilla-inject.undraggable", timeout=1
                        ):
                            self._click_button(
                                (By.CSS_SELECTOR, "h1.gorilla-inject.undraggable")
                            )
                    except:
                        continue

            def I_ClickLabel(label_locator, clickable_button: bool = False):
                logging.info("<<< Clicking label >>>")
                while self.running:
                    try:
                        if self._visible_section(f"{label_locator}", timeout=0.2):
                            self._click_label(
                                f"{label_locator}", clickable=clickable_button
                            )
                    except:
                        continue

            def I_EnterText(input_locator, value, clickable_button: bool = False):
                logging.info("<<< Entering text value >>>")
                while self.running:
                    try:
                        if self._visible_section(
                            f"input[name='{input_locator}']", timeout=0.2
                        ):
                            InitialValue = self.driver.find_element(
                                "input[name='{input_locator}']"
                            ).get_attribute("value")
                            print("initial value", value)
                            if not InitialValue:
                                self._enter_text(
                                    f"input[name='{input_locator}']",
                                    value,
                                    clickable_button,
                                )
                            else:
                                if clickable_button:
                                    self._click_button()
                    except:
                        continue

            I_QuestionThread = threading.Thread(target=I_Question)
            I_GorillaThread = threading.Thread(target=I_Gorilla)
            I_SliderRangeThread = threading.Thread(target=I_SliderRange)
            NextButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("NextButton",)
            )
            I_InstructionVideoThread = threading.Thread(target=I_InstructionVideo)
            ContinueButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("continue-button",)
            )
            StartButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("start-button",)
            )
            MediaAccessButtonThread = threading.Thread(
                target=I_ButtonSetup, args=("media-access-check",)
            )
            # 116, Review before continuing
            # label[for='QR~QID650~1']#QID650-1-label
            ReviewLabelThread = threading.Thread(
                target=I_ClickLabel, args=("label[for='QR~QID650~1']#QID650-1-label",)
            )
            # 117, Email Address
            EmailThread = threading.Thread(
                target=I_EnterText,
                args=(
                    "QR~QID117~TEXT",
                    self.email,
                    True,
                ),
            )
            # 777, Legal Name
            LegalNameThread = threading.Thread(
                target=I_EnterText,
                args=(
                    "QR~QID777~TEXT",
                    f"{self.first_name} {self.last_name}",
                    True,
                ),
            )
            # 778, Date of birth
            DobThread = threading.Thread(
                target=I_EnterText,
                args=(
                    "QR~QID778~TEXT",
                    self.date_of_birth,
                    True,
                ),
            )
            # retain mail for further research
            RetainEmailThread = threading.Thread(
                target=I_ClickLabel,
                args=(
                    "label[for='QR~QID748~1']#QID748-1-label",
                    True,
                ),
            )
            # password and confirm password
            PasswordThread = threading.Thread(
                target=I_EnterText,
                args=(
                    "QR~QID178~TEXT",
                    self.password,
                ),
            )
            ConfirmPasswordThread = threading.Thread(
                target=I_EnterText,
                args=("QR~QID196~TEXT", self.password, True),
            )

            logging.info("... starting thread ...")
            I_QuestionThread.start()
            I_GorillaThread.start()
            I_SliderRangeThread.start()
            I_InstructionVideoThread.start()
            ReviewLabelThread.start()
            EmailThread.start()
            LegalNameThread.start()
            DobThread.start()
            RetainEmailThread.start()
            PasswordThread.start()
            ConfirmPasswordThread.start()
            NextButtonThread.start()
            ContinueButtonThread.start()
            StartButtonThread.start()
            MediaAccessButtonThread.start()

            logging.info("... joining thread ...")
            I_QuestionThread.join()
            I_GorillaThread.join()
            I_SliderRangeThread.join()
            I_InstructionVideoThread.join()
            ReviewLabelThread.join()
            EmailThread.join()
            LegalNameThread.join()
            DobThread.join()
            RetainEmailThread.join()
            PasswordThread.join()
            ConfirmPasswordThread.join()
            NextButtonThread.join()
            ContinueButtonThread.join()
            StartButtonThread.join()
            MediaAccessButtonThread.join()
        except:
            print(f"<< problem continue the conferencing: {traceback.format_exc()} >>>")
            self.teardown_method()
        finally:
            print("<<< Ending the conferencing >>>")


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
    test = Qualification(email=email, password=password, person=person)
    test.setup_method()
    try:
        test.start()
    finally:
        logging.info(f"Finished process for {email}")
        test.teardown_method()
        time.sleep(4)  # Introduce a delay to minimize CPU and network strain


if __name__ == "__main__":
    accounts = [
        # Add more accounts as needed
    ]
    run_in_batches(accounts)
