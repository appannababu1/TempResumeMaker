import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

res = requests.get("https://www.canva.com/design/DAGmF74sGS4/F0yjhSbMaRJkN0vWZ5vC9A/view?embed", headers=header)
soup = BeautifulSoup(res.text, 'html.parser')

with open("resume.html", "w", encoding="utf-8") as file:
    file.write(res.text)

import os
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright
import hashlib
import re

def safe_filename(url, max_length=150):
    parsed = urlparse(url)
    path = parsed.path.lstrip('/')

    # Replace unsafe chars
    safe_path = re.sub(r'[<>:"/\\|?*]', '_', path)

    # Include query string part (if any) in filename
    if parsed.query:
        safe_path += '_' + re.sub(r'[<>:"/\\|?*]', '_', parsed.query)

    # Limit length to avoid OSError
    if len(safe_path) > max_length:
        # fallback to hash of full URL
        hash_digest = hashlib.sha1(url.encode()).hexdigest()
        ext = os.path.splitext(path)[-1]
        safe_path = f'resource_{hash_digest}{ext}'

    if not safe_path:
        safe_path = "index.html"
    return safe_path

def save_resource(url, content, output_dir):
    filename = safe_filename(url)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(content)
    print(f"Saved {url} -> {filepath}")

def download_page_and_assets(html_content, output_dir='saved_page'):
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        resources = {}

        # Intercept all requests and save responses
        def on_response(response):
            try:
                if response.request.resource_type in ["document", "stylesheet", "script", "image", "font"]:
                    url = response.url
                    content = response.body()
                    resources[url] = content
            except Exception as e:
                print(f"Error fetching {response.url}: {e}")

        page.on("response", on_response)

        # Load HTML content
        page.set_content(html_content, wait_until='networkidle')

        # Save main page content
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page.content())

        # Save all resources
        for url, content in resources.items():
            save_resource(url, content, output_dir)

        browser.close()

# Example HTML
html_content = res.text
download_page_and_assets(html_content, output_dir='saved_page')
