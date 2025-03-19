import hashlib
import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

from linkedin_scraper.scraper.validator import validate_session_cookies


class Login:
    """
    Handles LinkedIn login and session management using Selenium.
    Caches session cookies to minimize re-authentication.
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cookies = self.get_cookie()

    def get_cookie(self) -> dict:
        """
        Retrieves LinkedIn session cookies,
        either from cache or by logging in.
        Returns:
            dict: Cookies
        """

        # Fetching cookies from cache
        cached_cookies = self._load_cookies_from_cache()
        valid = validate_session_cookies(cached_cookies)
        if cached_cookies and valid:
            # If cookies existed in the cache
            # and it's valid, return it.
            return cached_cookies

        # Initiating the login process with selenium
        driver = self._launch_browser()
        cookies = self._authenticate(driver=driver)
        driver.close()
        return cookies

    def _launch_browser(self) -> object:
        """
        Launches a Chrome browser instance with anti-detection settings.
        Returns:
            object: Driver object
        """

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        stealth(driver, languages=["en-US", "en"], platform="Linux")
        return driver

    def _authenticate(self, driver):
        """
        Performs LinkedIn login and retrieves authentication cookies.
        Args:
            driver: Driver Object
        Returns:
            dict: Cookies
        """

        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Entering the Email
        email_element = driver.find_element(By.ID, "username")
        email_element.send_keys(self.email)

        # Entering password
        password_element = driver.find_element(By.ID, "password")
        password_element.send_keys(self.password)
        password_element.submit()

        # Waiting for the page to load completly
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "global-nav__primary-link"))
        )

        raw_cookies = driver.get_cookies()
        self._cache_cookies(raw_cookies)
        cookies = self._clean_cookies(raw_cookies)
        return cookies

    def _convert_credentials_to_hash(self):
        # Hashing the email-password combination
        credentials = f"{self.email}|{self.password}"
        return hashlib.md5(credentials.encode()).hexdigest()

    def _cache_cookies(self, cookies):
        """
        Stores authentication cookies in a local JSON cache file.
        """

        # Setting up the path
        BASE_PATH = os.path.dirname(__file__)
        filaname_id = self._convert_credentials_to_hash()
        filaname = f".cache/{filaname_id}.json"
        cookie_cache_path = os.path.join(BASE_PATH, filaname)

        # Writing cookie-dict as JSON file
        with open(cookie_cache_path, "w") as file:
            json.dump(cookies, file, indent=4)

    def _load_cookies_from_cache(self):
        """
        Loads cached authentication cookies if available.
        """

        # Setting up the path
        BASE_PATH = os.path.dirname(__file__)
        filaname_id = self._convert_credentials_to_hash()
        filaname = f".cache/{filaname_id}.json"
        cookie_cache_path = os.path.join(BASE_PATH, filaname)

        # Checking if the file exists
        if not os.path.exists(cookie_cache_path):
            return {}

        # Reading the cookie only if exists.
        with open(cookie_cache_path, "r") as file:
            raw_cookies = json.load(file)
            cookies = self._clean_cookies(raw_cookies)
            return cookies

    def _clean_cookies(self, raw_cookies):
        """
        Filters and extracts only the necessary authentication cookies.
        """
        if not raw_cookies:
            return {}

        required_cookies = [
            "bcookie",
            "lang",
            "liap",
            "JSESSIONID",
            "bscookie",
            "li_at",
        ]
        cookies = {}
        for cookie in raw_cookies:
            cookie_name = cookie["name"]
            if not cookie_name in required_cookies:
                continue

            cookie_value = cookie["value"]
            cookies[cookie_name] = cookie_value

        return cookies
