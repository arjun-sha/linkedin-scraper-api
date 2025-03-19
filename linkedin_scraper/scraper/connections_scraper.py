import asyncio
from copy import deepcopy

from dynaconf_config import settings
from linkedin_scraper.scraper.login import Login
from linkedin_scraper.scraper.parser import LinkedinParser
from linkedin_scraper.scraper.profile_scraper import LinkedinProfileScraper
from linkedin_scraper.scraper.requests import Request
from linkedin_scraper.scraper.utils import (decode_pagination_id,
                                            encode_pagination_id,
                                            extract_public_identifier,
                                            get_headers)
from tenacity import retry, stop_after_attempt


class LinkedinConnectionsScraper:
    def __init__(self, email, password, pagination_id: str = None):
        self.email = email
        self.password = password
        self.pagination_id = pagination_id
        self.session = Login(email=self.email, password=self.password)
        self.cookies = self.session.get_cookie()
        self.request = Request()

    @retry(stop=stop_after_attempt(settings.RETRY))
    async def _get_listing_data(self, page_number):
        """
        Extracts the connections profile IDs
        and returns it as a list
        """
        start_index = 40 * page_number
        params = {
            "decorationId": "com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-16",
            "count": "40",
            "q": "search",
            "sortType": "RECENTLY_ADDED",
            "start": str(start_index),
        }

        # Sending API request
        api_url = "https://www.linkedin.com/voyager/api/relationships/dash/connections"
        headers = deepcopy(get_headers(header_type="profile_page"))
        headers["csrf-token"] = self.cookies["JSESSIONID"].replace('"', "").strip()
        response = await self.request.fetch(
            url=api_url, params=params, headers=headers, cookies=self.cookies
        )

        # Extracting profiles-ids of the connections
        parser = LinkedinParser(response)
        connections_profile_ids = parser.extract_connections_profile_ids()
        return connections_profile_ids

    async def get_connections_data(self):
        """
        This is the main function that calls the `_get_listing_data`
        and sending async-requests with thread-lock to scrape all the data.
        """

        # Getting pagenumber from pagination_id
        page_number = (
            decode_pagination_id(self.pagination_id)
            if self.pagination_id
            else 0
        )

        # Extracting the listings of the profiles in the connections
        connections_profile_ids = await self._get_listing_data(page_number=page_number)
        # Scraping all the profile data
        profile_data = await self.scrape_profile_data(connections_profile_ids)

        # Setting up next pagination ID
        next_page_number = page_number + 1
        next_pagination_id = encode_pagination_id(next_page_number)

        connections_data = {
            "profiles": profile_data,
            "pagination_id": next_pagination_id,
        }
        return connections_data

    async def scrape_profile_data(self, connections_profile_ids):
        """
        Scraping a list of profile pages, with thread-locking system
        `Semaphone`. Max-Worker is 5. It will return the profile data
        as list.
        """
        scraper = LinkedinProfileScraper(email=self.email, password=self.password)

        semaphore = asyncio.Semaphore(5)
        async def worker(profile_id):
            async with semaphore:
                await scraper.get_profile_data(public_identifier=profile_id)

        tasks = [worker(profile_id) for profile_id in connections_profile_ids]
        profile_data = await asyncio.gather(*tasks)
        return profile_data
