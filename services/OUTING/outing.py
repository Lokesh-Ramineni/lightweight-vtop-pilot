from enpoints import OUTING
from OUTING.parser import check_outing
from src.session import build_cookies
import httpx
async def apply_outing(client,vtop_engine,data):
    
    res=client.post(OUTING,cookies=build_cookies(vtop_engine),data=data)
    

    

    