from enpoints import PRE_LOGIN

async def get_prelogin(client,prelog_data):
    prelog= await client.post(PRE_LOGIN,data=prelog_data)
    return prelog