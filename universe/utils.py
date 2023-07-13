import requests

from core.logger import logger
from main.models import Settings

from .models import Article


def get_active_data_url() -> str or None:
    try:
        return Settings.objects.get(is_active=True).data_url
    except Settings.DoesNotExist:
        logger.error("No active Settings found")
        return None


def fetch_data(url: str) -> dict or None:
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        logger.error(e)
        return None


def get_icon_url(article: Article):
    types_url = f"https://images.evetech.net/types/{article.eve_id}"
    types = fetch_data(types_url)
    if types:
        set_icon_urls(article, types)


def set_icon_urls(article: Article, types: dict):
    if "render" in types:
        article.render_url = (
            f"https://images.evetech.net/types/{article.eve_id}/render?size=512"
        )

    if "bp" in types:
        article.icon_url = f"https://images.evetech.net/types/{article.eve_id}/bp"
    elif "relic" in types:
        article.icon_url = f"https://images.evetech.net/types/{article.eve_id}/relic"
    elif "reaction" in types:
        article.icon_url = f"https://images.evetech.net/types/{article.eve_id}/reaction"
    else:
        article.icon_url = f"https://images.evetech.net/types/{article.eve_id}/icon"
