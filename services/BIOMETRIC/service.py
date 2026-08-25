from enpoints import BIOMETRIC_INFO
from services.BIOMETRIC.parser import fetch_bio
import httpx
async def get_biometric(client,vtop_engine,data5):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)
    try:
        r=await client.post(BIOMETRIC_INFO,cookies=ck,data=data5,timeout=10)
    except TimeoutError as e:
        print(f"Error occured:{e}")
    fetch_bio(r.text)