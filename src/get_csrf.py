
import re
def get_csrf(html_src) -> tuple[str, str | None] | None:
    csrf_token = re.search(r'name="_csrf"\s+value="([^"]+)"', html_src)
    flag = re.search(r'name="flag"\s+value="([^"]+)"', html_src)
    if not csrf_token:
        return None
    if flag:
        flag_value = flag.group(1)
    else:
        return None

    return csrf_token.group(1), flag_value

def get_csrf_token(html_src: str) -> str | None:
    csrf_token = re.search(r'name="_csrf"\s+value="([^"]+)"', html_src)
    if not csrf_token:
        return None
    return csrf_token.group(1)