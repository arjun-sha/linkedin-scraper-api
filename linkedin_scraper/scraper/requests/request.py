from curl_cffi.requests import AsyncSession
from curl_cffi.requests.errors import CurlError, RequestsError
from linkedin_scraper.exceptions import RequestFailedException
from linkedin_scraper.scraper.requests.abstract import AbstractRequest
from linkedin_scraper.scraper.requests.response import Response
from linkedin_scraper.scraper.requests.utils import (add_user_agent,
                                                     get_browser_details,
                                                     shuffle_headers)


class Request(AbstractRequest):
    async def fetch(
        self,
        method: str = "GET",
        url: str = None,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        cookies: dict = None,
    ):
        """
        Sends an asynchronous HTTP request with randomized headers and browser impersonation.
        Uses curl_cffi to perform an HTTP request while spoofing browser details and shuffling headers.
        Handles CurlError and RequestsError, raising RequestFailedException on failure.

        Args:
            method (str, optional): HTTP method (e.g., "GET", "POST"). Defaults to "GET".
            url (str, optional): Target URL. Defaults to None.
            data (dict, optional): Payload for POST/PUT requests. Defaults to None.
            params (dict, optional): Query parameters. Defaults to None.
            headers (dict, optional): Custom headers. Defaults to None.
            cookies (dict, optional): Cookies. Defaults to None.

        Returns:
            Response: Custom Response object with status_code, content, text, headers, and cookies.
        """

        # Randomizing browser impersonates and user-agent
        browser_details = get_browser_details()
        headers = add_user_agent(headers, browser_details)
        headers = shuffle_headers(headers)

        # Sending HTTP request in async mode
        async with AsyncSession() as session:
            try:
                response = await session.request(
                    url=url,
                    data=data,
                    timeout=60,
                    params=params,
                    method=method,
                    headers=headers,
                    cookies=cookies,
                    impersonate=browser_details["impersonate"],
                )

            except (CurlError, RequestsError) as exe:
                error_message = "Curl-CFFI failed to send request - %s" % exe
                raise RequestFailedException(error_message)

        # Returning custom response wrapper
        custom_response = Response(
            status_code=response.status_code,
            content=response.content,
            text=response.text,
            headers=response.headers,
            cookies=response.cookies,
        )
        return custom_response
