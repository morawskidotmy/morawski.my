import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape

import requests

SERVICES_FILE = "./services.json"
OUTPUT_FILE = "./index.html"
TEMPLATE_FILE = "./template.html"
BLSKY_RSS_URL = "https://bsky.app/profile/morawski.my/rss"
MAX_BLOG_POSTS = 3


def load_services():
    with open(SERVICES_FILE) as file:
        return json.load(file)["services"]


def fetch_bluesky_posts():
    try:
        with urllib.request.urlopen(BLSKY_RSS_URL, timeout=10) as response:
            feed = ET.parse(response).getroot()
        items = feed.findall("./channel/item")
        posts = []
        for item in items[:MAX_BLOG_POSTS]:
            description = item.findtext("description") or ""
            posts.append({"description": description})
        return posts
    except (OSError, ET.ParseError):
        return []


def check_service_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def generate_html(services, bluesky_posts):
    with open(TEMPLATE_FILE) as template_file:
        content = template_file.read()

    service_status_html = ""
    for service in services:
        status = "Online" if check_service_status(service["url"]) else "Offline"
        response_code = "200" if status == "Online" else ""
        service_status_html += f"""
            <div class="bento-box status-{status.lower()}">
                <strong>{service["name"]}</strong><br>
                Status: {status}<br>
                {"Response Code: " + response_code if response_code else ""}
            </div>
        """

    blog_posts_html = ""
    for post in bluesky_posts:
        blog_posts_html += f"""
            <div class="bento-box blog-post">
                <strong>{escape(post["description"])}</strong>
            </div>
        """
    blog_posts_html += """
            <div class="bento-box blog-post">
                <a href="https://bsky.app/profile/morawski.my">
                    <strong>Follow on Bluesky →</strong>
                </a>
            </div>
        """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_content = content.replace("<!-- services -->", service_status_html)
    final_content = final_content.replace("<!-- blogs -->", blog_posts_html)
    final_content = final_content.replace("{last_updated}", current_time)

    return final_content


def main():
    while True:
        bluesky_posts = fetch_bluesky_posts()
        services = load_services()
        html_content = generate_html(services, bluesky_posts)

        with open(OUTPUT_FILE, "w") as output_file:
            output_file.write(html_content)

        print(f"Updated {OUTPUT_FILE} successfully.")
        time.sleep(60)


if __name__ == "__main__":
    main()
