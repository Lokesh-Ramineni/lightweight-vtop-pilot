from enpoints import POST_PRE_LOGIN
async def get_post_prelogin(client,payload):
    # print("Before login:", client.cookies)
    post_pre_login=await client.post(POST_PRE_LOGIN,data=payload)

    # print("After login:", client.cookies)
    return post_pre_login