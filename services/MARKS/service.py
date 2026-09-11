import httpx
import logging
from pathlib import Path
from enpoints import MARKS_INFO
from src.session import build_cookies
from services.MARKS.parser import fetch_marks

ROOT_DIR=Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"

logger=logging.getLogger(__name__)
async def get_marks(client,vtop_engine,data4):
    logger.info("Requesting marks data")

    try:
        r=await client.post(MARKS_INFO,data=data4,cookies=build_cookies(vtop_engine))
        r.raise_for_status()

    except httpx.HTTPError as e:
        logger.error(f"Marks request failed: {e}")
        return

    except Exception as e:
        logger.error(f"Unexpected error while fetching marks: {e}")
        return

    try:
        fetch_marks(r.text)
        logger.info("Marks fetched successfully")

    except Exception as e:
        logger.error(f"Failed to parse marks data: {e}")

    # with open(timetable_path/"marks.html","wb") as f:
    #     f.write(r.content)