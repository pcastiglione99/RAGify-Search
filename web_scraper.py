import os
import re
import base64
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def fetch_web_pages(query: str, download_dir: str = "./downloaded"):
    os.makedirs(download_dir, exist_ok=True)
    for result in search(query, lang="en", region="us"):
        try:
            response = requests.get(result, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.find("body").get_text(strip=True)
            text = re.sub(r'\s{2,}', '\n', text)

            local_filename = base64.b64encode(result.encode("utf-8")).decode()
            with open(os.path.join(download_dir, local_filename), "w", encoding="utf-8") as f:
                f.write(text)
        except (requests.RequestException, AttributeError):
            continue

def remove_temp_files(download_dir: str = "./downloaded"):
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        os.remove(file_path)

