from copy import deepcopy

from tenacity import retry, stop_after_attempt

from dynaconf_config import settings
from linkedin_scraper.scraper.login import Login
from linkedin_scraper.scraper.parser import LinkedinParser
from linkedin_scraper.scraper.requests import Request
from linkedin_scraper.scraper.utils import (extract_public_identifier,
                                            get_headers)


class LinkedinProfileScraper:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = Login(email=self.email, password=self.password)
        self.cookies = self.session.get_cookie()
        self.request = Request()

    @retry(stop=stop_after_attempt(10))
    async def get_profile_data(self, public_identifier: str=None,
                               uri: str=None):
        """
        Main function to extract the profile data
            - If public_id/uri not given, assume that it should scrape the logged-in user.
            - In the above case, it will send a homepage request to extract the public-id.
            - It will scrape basic details and contact details and return as a string

        Returns: dict: Scraped Data
        """
        if not public_identifier and not uri:
            # If public id is not provided, Assume that
            # It should scrape the profile of the logged in user.
            public_identifier = await self._get_public_identifier()

        api_profile_url = (
            "https://www.linkedin.com/voyager/api/identity"
            f"/profiles/{public_identifier}/profileView"
        )

        # Sending the Voyagor API requests to get the profile details
        headers = deepcopy(get_headers(header_type="profile_page"))
        headers["csrf-token"] = self.cookies["JSESSIONID"].replace('"', "").strip()
        response = await self.request.fetch(
            url=api_profile_url,
            headers=headers,
            cookies=self.cookies
        )

        # Extracting necessary Data
        parser = LinkedinParser(response)
        profile_data = parser.extract_profile_data()
        conatct_details = await self._get_contact_details(public_identifier)
        profile_data.update(conatct_details)
        return profile_data

    @retry(stop=stop_after_attempt(10))
    async def _get_contact_details(self, public_identifier):
        """
        Send API request to the contact details and return the data as dict.
        """
        api_profile_url = (
            "https://www.linkedin.com/voyager/api/identity"
            f"/profiles/{public_identifier}/profileContactInfo"
        )

        headers = deepcopy(get_headers(header_type="profile_page"))
        headers["csrf-token"] = self.cookies["JSESSIONID"].replace('"', "").strip()
        response = await self.request.fetch(
            url=api_profile_url,
            headers=headers,
            cookies=self.cookies
        )

        # Extracting necessary Data
        parser = LinkedinParser(response)
        contact_details = parser.extract_contact_details()
        return contact_details

    async def _get_public_identifier(self):
        """
        Send a homepage requests with the loggedin cookies
        to retrive the logged-in profile ID
        """
        homepage_url = "https://www.linkedin.com"
        headers = deepcopy(get_headers(header_type="homepage"))
        response = await self.request.fetch(
            method="GET",
            url=homepage_url,
            headers=headers,
            cookies=self.cookies
        )
        public_identifier = extract_public_identifier(response)
        return public_identifier
