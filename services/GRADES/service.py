import httpx
import logging
from enpoints import GRADES_INFO
from services.GRADES.parser import fetch_grades
from src.session import build_cookies


logger=logging.getLogger(__name__)

async def get_grades(client,vtop_engine,data4,csrf,semsub_id,username):
    logger.info("Requesting grades data")
    try:
        r=await client.post(GRADES_INFO,cookies=build_cookies(vtop_engine),data=data4)
        r.raise_for_status()

    except httpx.HTTPError as e:
        logger.error(f"Grades request failed: {e}")
        return

    except Exception as e:
        logger.error(f"Unexpected error while fetching grades: {e}")
        return

    try:
        await fetch_grades(r.text,client,vtop_engine,csrf,semsub_id,username)
        logger.info("Grades request successfully")
    except Exception as e:
        logger.error(f"Failed to parse grades data: {e}")