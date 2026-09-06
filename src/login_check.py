from bs4 import BeautifulSoup
def login_ch(html_src):
    soup = BeautifulSoup(html_src, 'lxml')
    check = soup.find("h4", class_="fw-bold")
    return check is not None and "VTOP Login" in check.get_text()
