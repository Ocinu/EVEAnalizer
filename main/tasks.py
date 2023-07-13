import uuid
import xml.etree.ElementTree as ET

import requests

from core.celery import app as celery_app
from core.logger import logger
from main.models import News


@celery_app.task
def update_eve_news():
    response = requests.get("https://www.eveonline.com/rss")
    if response.status_code != 200:
        logger.error(f"Update news error {response.status_code}")
        return None
    else:
        root = ET.fromstring(response.content)
        existing_news_links = set(News.objects.values_list("link", flat=True))

        new_news = [
            News(
                id=uuid.uuid5(uuid.NAMESPACE_URL, item.find("link").text),
                title=item.find("title").text,
                link=item.find("link").text,
                description=item.find("description").text,
                published=item.find("pubDate").text,
            )
            for item in root.findall(".//item")
            if item.find("link").text not in existing_news_links
        ]

        News.objects.bulk_create(new_news)
