import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from linkedin_scraper.auth.authenticator import authenticate
from linkedin_scraper.scraper.connections_scraper import \
    LinkedinConnectionsScraper
from linkedin_scraper.scraper.profile_scraper import LinkedinProfileScraper
from linkedin_scraper.web.schema import ConnectionsModel, ProfileModel

router = APIRouter()


@router.post("/api/connections")
async def get_connections_data(item: ConnectionsModel):
    valid_call = authenticate(item)
    if not valid_call:
        return JSONResponse(content={"Hi": "Failed"},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    scraper = LinkedinConnectionsScraper(
        email=item.email,
        password=item.password,
        pagination_id=item.pagination_id
    )
    connections_profile_data = await scraper.get_connections_data()
    return JSONResponse(content=connections_profile_data, status_code=status.HTTP_200_OK)

@router.post("/api/profile")
async def get_profile_data(item: ProfileModel):
    valid_call = authenticate(item)
    if not valid_call:
        return JSONResponse(content={"Hi": "Failed"},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    scraper = LinkedinProfileScraper(
        email=item.email,
        password=item.password
    )
    profile_data = await scraper.get_profile_data()
    return JSONResponse(content=profile_data,
                            status_code=status.HTTP_200_OK)
