import httpx
import logging
from enpoints import BIOMETRIC_INFO
from src.session import build_cookies
from services.BIOMETRIC.parser import fetch_bio

logger = logging.getLogger(__name__)

async def get_biometric(client,vtop_engine,data5):

    try:
        r=await client.post(BIOMETRIC_INFO,cookies=build_cookies(vtop_engine),data=data5,timeout=10)
        r.raise_for_status()
        
        fetch_bio(r.text)
    except httpx.HTTPError as e:
        logger.error("Failed to fetch biometric information: %s", e)
        return None

    except Exception:
        logger.exception("Unexpected error while fetching biometric information")
        return None
    