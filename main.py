import os
import json
import time
import requests
from datetime import datetime

ARTICLES_DIR = './articles'
SERVICES_FILE = './services.json'
OUTPUT_FILE = './index.html'
TEMPLATE_FILE = './template.html'

def load_services():
    with open(SERVICES_FILE, 'r') as file:
        return json.load(file)['services']

def check_service_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def generate_html(services, articles):
    with open(TEMPLATE_FILE, 'r') as template_file:
        content = template_file.read()

    service_status_html = ""
    for service in services:
        status = "Online" if check_service_status(service['url']) else "Offline"
        response_code = "200" if status == "Online" else ""
        service_status_html += f"""
            <div class="bento-box status-{status.lower()}">
                <strong>{service['name']}</strong><br>
                Status: {status}<br>
                {"Response Code: " + response_code if response_code else ""}
            </div>
        """

    blog_posts_html = ""
    for article in articles:
        article_path = os.path.join(ARTICLES_DIR, article)
        blog_posts_html += f"""
            <div class="bento-box blog-post">
                <a href="{article_path}"><strong>{article}</strong></a>
            </div>
        """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_content = content.replace("<!-- services -->", service_status_html)
    final_content = final_content.replace("<!-- blogs -->", blog_posts_html)
    final_content = final_content.replace("{last_updated}", current_time)

    return final_content

def main():
    while True:
        articles = [f for f in os.listdir(ARTICLES_DIR) if os.path.isfile(os.path.join(ARTICLES_DIR, f))]
        services = load_services()
        html_content = generate_html(services, articles)

        with open(OUTPUT_FILE, 'w') as output_file:
            output_file.write(html_content)

        print(f"Updated {OUTPUT_FILE} successfully.")
        time.sleep(60)

if __name__ == "__main__":
    main()
