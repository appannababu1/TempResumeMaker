import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

res = requests.get("https://www.canva.com/design/DAGmF74sGS4/F0yjhSbMaRJkN0vWZ5vC9A/view?embed", headers=header)
soup = BeautifulSoup(res.text, 'html.parser')

with open("template.html", "w", encoding="utf-8") as file:
    file.write(res.text)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    html_content = res.text
    page.set_content(html_content)

    # Let scripts run automatically (it does by default)
    rendered_html = page.content()
    # print(rendered_html)

    with open("template.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)

    browser.close()
