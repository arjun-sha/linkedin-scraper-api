import random
from itertools import cycle

from dynaconf_config import settings
from linkedin_scraper.scraper.requests.user_agents import USER_AGENTS


def get_browser_details():
    """
    Returns a randomly selected browser and version for impersonation.
    The function selects from a predefined list of browsers and
    versions to simulate different user environments.

    Returns:
        dict: A dictionary containing:
              - 'impersonate' (str): The impersonation string.
              - 'browser' (str): The browser type
              - 'version' (str): The browser version (e.g., "110", "99", "15").
    """
    browser_versions = [
        {"impersonate": "chrome110", "browser": "chrome", "version": "110"},
        {"impersonate": "chrome107", "browser": "chrome", "version": "107"},
        {"impersonate": "chrome104", "browser": "chrome", "version": "104"},
        {"impersonate": "chrome101", "browser": "chrome", "version": "101"},
        {"impersonate": "chrome100", "browser": "chrome", "version": "100"},
        {"impersonate": "chrome99", "browser": "chrome", "version": "99"},
        {"impersonate": "edge99", "browser": "edge", "version": "99"},
        {"impersonate": "edge101", "browser": "edge", "version": "101"},
        {"impersonate": "safari15_3", "browser": "safari", "version": "15"},
        {"impersonate": "safari15_5", "browser": "safari", "version": "15"},
        {"impersonate": "safari15_5", "browser": "safari", "version": "15"},
    ]
    return random.choice(browser_versions)


def add_user_agent(headers, browser_details):
    browser = browser_details["browser"]
    version = browser_details["version"]
    user_agent = random.choice(USER_AGENTS[browser][version])
    headers["user-agent"] = user_agent
    return headers


def shuffle_headers(headers):
    headers_items = list(headers.items())
    random.shuffle(headers_items)
    shuffled_headers = dict(headers_items)
    return shuffled_headers


def get_proxies():
    proxy_1 = settings.PROXY_1
    proxy_2 = settings.PROXY_2
    proxy_3 = settings.PROXY_3

    proxies = [proxy_1, proxy_2, proxy_3]
    proxies = [i for i in proxies if proxies != "None"]
    proxies = [{"http": i, "https": i} for i in proxies]
    return cycle(proxies)
