import httpx
import logging
from src.session import build_cookies
from enpoints import STUDENT_DETAILS
from services.DETAILS.parser import parse_details

logger=logging.getLogger(__name__)

async def get_details(client,vtop_engine,data1):
    try:
        r=await client.post(STUDENT_DETAILS,cookies=build_cookies(vtop_engine),data=data1)
        r.raise_for_status()

        parse_details(r.text)
        
    except httpx.HTTPError as e:
        logger.error("Failed to fetch student details: %s", e)
        return None

    except Exception:
        logger.exception("Unexpected error while fetching student details")
        return None