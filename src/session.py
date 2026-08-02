from enpoints import CONTENT
import httpx
async def cookie_check(client,cookie):
    ck=httpx.Cookies()
    ck.set("JSESSIONID",cookie)
    chk=await client.get(CONTENT,cookies=ck)
    return chk,str(chk.url)