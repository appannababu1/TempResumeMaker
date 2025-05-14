from playwright.sync_api import sync_playwright

html_content = open("template.html", "r", encoding="utf-8").read()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content)
    page.pdf(path="output.pdf", format="A4", print_background=True)
    browser.close()