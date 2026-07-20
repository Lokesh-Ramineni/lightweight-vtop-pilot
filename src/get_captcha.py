import base64
import re
from pathlib import Path
from enpoints import POST_PRE_LOGIN

ROOT_DIR = Path(__file__).resolve().parent.parent
# Ensure directory setup is safe
CAPTCHA_FOLDER = ROOT_DIR / "captcha"
captcha_dir = CAPTCHA_FOLDER / "captcha.png"


async def get_captcha(html_src, client):
    # Proactively prevent FileNotFoundError
    CAPTCHA_FOLDER.mkdir(parents=True, exist_ok=True)

    curr_html = html_src
    img_pattern = r'<img[^>]*src="data:image/[^;]+;base64,([^"]+)"'

    match = re.search(img_pattern, curr_html, re.DOTALL)
    # print(client.cookies)
    if match is None:
        while True:
            # 1. Fetch fresh payload data first
            print("Image not found, reloading...")
            new_response = await client.get(POST_PRE_LOGIN)
            curr_html = new_response.text

            # 2. Evaluate the newly pulled HTML context immediately
            match = re.search(img_pattern, curr_html, re.DOTALL)
            if match:
                print("Image found successfully!")
                break

    # Safely write binary string matching your core blueprint
    decoded = base64.b64decode(match.group(1))
    with open(captcha_dir, "wb") as f:
        f.write(decoded)
    # print(client.cookies)
    return client, curr_html
