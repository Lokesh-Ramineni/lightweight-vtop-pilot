from enpoints import BIOMETRIC_INFO
from services.BIOMETRIC.parser import fetch_bio
from src.session import build_cookies
import httpx
async def get_biometric(client,vtop_engine,data5):

    try:
        r=await client.post(BIOMETRIC_INFO,cookies=build_cookies(vtop_engine),data=data5,timeout=10)
    except TimeoutError as e:
        print(f"Error occured:{e}")
    fetch_bio(r.text)