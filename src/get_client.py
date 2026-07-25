import httpx
from enpoints import VTOP_BASE_URL,HEADERS
def get_client():
    client = httpx.AsyncClient(base_url=VTOP_BASE_URL,headers=HEADERS,follow_redirects=True,verify=False)
    return client