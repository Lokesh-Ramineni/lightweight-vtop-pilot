import re
def check(html_src):
    user = re.search(r'<input[^>]*placeholder="Username"[\s\S]*?id="([^"]+)"\s+name="([^"]+)"', html_src)
    password=re.search(r'<input[^>]*placeholder="Password"[\s\S]*?id="([^"]+)"\s+name="([^"]+)"',html_src)

    if user and password:
        return True
    else:
        return False
