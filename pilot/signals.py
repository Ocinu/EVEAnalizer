from django.db.models.signals import post_save
from django.dispatch import receiver

from core.logger import logger
from universe.models import Article, SolarSystem
from universe.utils import fetch_data

from .models import Location


@receiver(post_save, sender=Location)
def create_location(sender, instance, created, **kwargs):
    if created:
        data = fetch_data(
            f"https://esi.evetech.net/latest/universe/stations/{instance.eve_id}"
        )
        if data:
            instance.name = data.get("name")
            instance.solar_system = SolarSystem.objects.get_or_create(
                eve_id=data.get("system_id")
            )[0]
            instance.type = Article.objects.get_or_create(eve_id=data.get("type_id"))[0]
            instance.save(update_fields=["name", "solar_system", "type"])
        else:
            logger.error(f"Solar system {instance.eve_id} get info error")
