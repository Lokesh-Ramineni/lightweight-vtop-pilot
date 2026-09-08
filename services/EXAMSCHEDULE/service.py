import httpx
import logging
from enpoints import EXAM_SCHEDULE
from src.session import build_cookies
from services.EXAMSCHEDULE.parser import parse_schedule

logger=logging.getLogger(__name__)

async def get_schedule(client,vtop_engine,data4):

    try:
        logger.info("Requesting Exam Schedule")
        r=await client.post(EXAM_SCHEDULE,cookies=build_cookies(vtop_engine),data=data4)
        r.raise_for_status()
        logger.info("Request Success")
        parse_schedule(r.text)

    except httpx.HTTPError as e:
        logger.error("Failed to fetch exam schedule: %s", e)
        return None

    except Exception:
        logger.exception("Unexpected error while fetching exam schedule")
        return None