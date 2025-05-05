from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os
import re

def is_file_exist(title_file):
    return os.path.exists(f'./{title_file}.pdf')

def preprocessing_file_name(file_name):
    name = re.sub(r"[\\/<>:\"|?*]","_", file_name)
    name = re.sub(r"\s+"," ", name).strip()
    return name


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs",{
    "download.default_directory": "./data_source",
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})

# Đường dẫn trang báo cáo
REPORT_URL = "https://vcbs.com.vn/bao-cao-tai-chinh"

# Khởi động trình duyệt
driver = webdriver.Chrome(options=options)
driver.get(REPORT_URL)

time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

report_cards = soup.find_all("div", class_="o-reportsCard_content")


for card in report_cards:
    title_tag = card.find("p")
    link_tag = card.find("a")
    title = title_tag.get_text() if title_tag else "No Title"
    link = link_tag["href"] if link_tag else "No Link"
    # link_tag.click()

    response = requests.get(REPORT_URL+link)
    with open(f"./data_source/{preprocessing_file_name(title)}.pdf", "wb") as f:
        f.write(response.content)

driver.quit()
