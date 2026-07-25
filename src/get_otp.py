from enpoints import OTP,VALIDATE_OTP
async def get_otp_pg(client):
    r=await client.get(OTP)
    print(r.url)
    return r

async def validate(client,data):
    r=await client.post(VALIDATE_OTP,data=data)
    print(r.url)
    return r

async def redirect(client,redirect_url):
    r=await client.get(redirect_url,follow_redirect=True)
    print(r.url)
    return r