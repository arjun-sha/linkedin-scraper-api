import base64
import json
import re


def get_headers(header_type: str) -> dict:
    """
    Retrieves predefined HTTP headers based on the specified type.

    Args:
        header_type (str): The type of headers to retrieve.
            - "homepage": Headers for accessing the LinkedIn homepage.
            - "profile_page": Headers for accessing a LinkedIn profile page.

    Returns:
        dict: A dictionary containing the appropriate HTTP headers.
    """
    headers_homepage = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }
    if header_type == "homepage":
        return headers_homepage

    headers_profile_page = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "accept-language": "en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-li-lang": "en_US",
        "x-restli-protocol-version": "2.0.0",
    }
    if header_type == "profile_page":
        return headers_profile_page


def extract_public_identifier(response) -> str:
    """
    Extracts the public identifier from a LinkedIn profile page response.

    Args:
        response (Response): The HTTP response object containing profile page data.

    Returns:
        str: The extracted public identifier, or None if not found.
    """
    regex_pattern = r'(publicIdentifier\&quot\;\:\&quot\;)(.*?)(\&quot\;)'
    try:
        public_identifier = re.search(regex_pattern, response.text).group(2)
        return public_identifier
    except Exception:
        return None


def encode_pagination_id(page_number: int) -> str:
    """
    Encodes a pagination ID for LinkedIn profile data navigation.

    Args:
        page_number (int): The page number to encode.

    Returns:
        str: A Base64-encoded string representing the pagination ID.
    """
    raw_data = {"next_page_number": page_number}
    raw_data = json.dumps(raw_data)
    pagination_id = base64.b64encode(raw_data.encode("utf-8")).decode("utf-8")
    return pagination_id


def decode_pagination_id(pagination_id: str) -> int:
    """
    Decodes a Base64-encoded pagination ID to retrieve the next page number.

    Args:
        pagination_id (str): The Base64-encoded pagination string.

    Returns:
        int: The extracted page number.
    """
    decoded_data = base64.b64decode(pagination_id).decode("utf-8")
    json_data = json.loads(decoded_data)
    next_page_number = int(json_data["next_page_number"])
    return next_page_number
