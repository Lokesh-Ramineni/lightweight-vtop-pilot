from enpoints import OUTING
from OUTING.parser import check_outing
import httpx
async def apply_outing(client,cookie,data):
    ck=httpx.Cookies()
    ck.set("JSESSIONID", cookie)
    res=client.post(OUTING,cookies=cookie,data=data)
    print(res.status_code)

    

    