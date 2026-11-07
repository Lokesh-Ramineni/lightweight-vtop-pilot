from bs4 import BeautifulSoup

def login_ch(html_src):
    soup = BeautifulSoup(html_src, "lxml")
    heading = soup.find("h4", class_="fw-bold")
    return heading is not None and "VTOP Login" in heading.get_text(strip=True)

def cap_check(html_src):
    soup = BeautifulSoup(html_src, "lxml")

    alert_span = soup.find("span", attrs={"role": "alert"})

    if alert_span:
        strong_tag = alert_span.find("strong")

        if strong_tag.get_text(strip=True)== "Invalid Captcha":
            return True
    return False


def is_otp_page(html_src):
    soup = BeautifulSoup(html_src, "lxml")

    otp_input = soup.find("input", attrs={"name": "otpCode"})

    page_text = soup.get_text(" ", strip=True).lower()
    otp_text = "additional verification required" in page_text

    return otp_input is not None or otp_text