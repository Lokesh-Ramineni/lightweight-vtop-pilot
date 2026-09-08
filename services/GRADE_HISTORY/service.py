import httpx
import logging
from enpoints import GRADE_HISTORY
from src.session import build_cookies
from services.GRADE_HISTORY.parser import fetch_grade_history

logger=logging.getLogger(__name__)
async def get_history(client,vtop_engine,data1):
    try:
        logger.info("Requesting Grade History")
        r=await client.post(GRADE_HISTORY,data=data1,cookies=build_cookies(vtop_engine))
        r.raise_for_status()
        logger.info("Request Success")
        
        fetch_grade_history(r.text)
    except httpx.HTTPError as e:
        logger.error("Failed to fetch grade history: %s", e)
        return None

    except Exception:
        logger.exception("Unexpected error while fetching grade history")
        return None