from enpoints import GRADES_INFO
from services.GRADES.parser import fetch_grades
from src.session import build_cookies
import httpx
async def get_grades(client,vtop_engine,data4,csrf,semsub_id,username):

    r=await client.post(GRADES_INFO,cookies=build_cookies(vtop_engine),data=data4)
    await fetch_grades(r.text,client,vtop_engine,csrf,semsub_id,username)