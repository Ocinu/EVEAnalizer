from django.db.models.signals import post_save
from django.dispatch import receiver

from core.logger import logger

from .models import (Article, Category, Constellation, Group, Region,
                     SolarSystem)
from .utils import fetch_data, get_active_data_url, get_icon_url


@receiver(post_save, sender=SolarSystem)
def create_solar_system(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(f"{data_url}/legacy/universe/systems/{instance.eve_id}/")
        if data:
            constellation = Constellation.objects.get_or_create(
                eve_id=data["constellation_id"]
            )[0]

            instance.name = data.get("name")
            instance.security_status = data.get("security_status")
            instance.constellation = constellation
            instance.save(update_fields=["name", "security_status", "constellation"])
        else:
            logger.error(f"Solar system {instance.eve_id} get info error")


@receiver(post_save, sender=Constellation)
def create_constellation(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(
            f"{data_url}/legacy/universe/constellations/{instance.eve_id}/"
        )
        if data:
            region = Region.objects.get_or_create(eve_id=data["region_id"])[0]

            instance.name = data.get("name")
            instance.region = region
            instance.save(update_fields=["name", "region"])
        else:
            logger.error(f"Constellation {instance.eve_id} get info error")


@receiver(post_save, sender=Region)
def create_region(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(f"{data_url}/legacy/universe/regions/{instance.eve_id}/")
        if data:
            instance.name = data.get("name")
            instance.save(update_fields=["name"])
        else:
            logger.error(f"Region {instance.eve_id} get info error")


@receiver(post_save, sender=Category)
def create_category(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(
            f"{data_url}/latest/universe/categories/{instance.eve_id}/?datasource=tranquility&language=en"
        )
        if data:
            instance.name = data.get("name")
            instance.save(update_fields=["name"])
        else:
            logger.error(f"Category {instance.eve_id} get info error")


@receiver(post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(
            f"{data_url}/latest/universe/groups/{instance.eve_id}/?datasource=tranquility&language=en"
        )
        if data:
            category = Category.objects.get_or_create(eve_id=data["category_id"])[0]

            instance.name = data.get("name")
            instance.category = category
            instance.save(update_fields=["name", "category"])
        else:
            logger.error(f"Group {instance.eve_id} get info error")


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if created:
        data_url = get_active_data_url()
        data = fetch_data(
            f"{data_url}/latest/universe/types/{instance.eve_id}/?datasource=tranquility&language=en"
        )
        if data:
            group = Group.objects.get_or_create(eve_id=data["group_id"])[0]

            instance.name = data.get("name")
            instance.group = group
            instance.description = data.get("description")
            instance.published = data.get("published")
            instance.packaged_volume = data.get("packaged_volume")
            instance.volume = data.get("volume")
            get_icon_url(instance)
            instance.save(
                update_fields=[
                    "name",
                    "group",
                    "description",
                    "published",
                    "packaged_volume",
                    "volume",
                ]
            )
        else:
            logger.error(f"Article {instance.eve_id} get info error")
