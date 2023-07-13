from core.celery import app as celery_app
from core.logger import logger
from universe.models import Article, Region, SolarSystem

from .auth import Auth
from .models import Character, Corporation, Location, MarketOrder


@celery_app.task
def update_current_orders():
    characters = Character.objects.all()
    for character in characters:
        url_current = (
            f"{Auth().settings.data_url}/legacy/characters/{character.eve_id}/orders/"
        )
        fetch_and_process_orders(url_current, character)

        url_history = f"{Auth().settings.data_url}/legacy/characters/{character.eve_id}/orders/history/"
        fetch_and_process_orders(url_history, character)


@celery_app.task
def update_wallet():
    auth = Auth()
    characters = Character.objects.all()
    for character in characters:
        wallet_data = auth.protected_access(
            f"{auth.settings.data_url}/legacy/characters/{character.eve_id}/wallet/",
            character,
        )
        if wallet_data:
            character.wallet_balance = wallet_data
            character.save(update_fields=["wallet_balance"])
        else:
            logger.error(f"{character.name} wallet not updated")


@celery_app.task
def update_characters():
    auth = Auth()
    characters = Character.objects.all()
    for character in characters:
        update_character(auth, character)


def fetch_and_process_orders(url: str, character: Character):
    auth = Auth()
    orders = auth.protected_access(url=url, character=character)

    order_id_set = set(
        MarketOrder.objects.filter(owner=character).values_list("order_id", flat=True)
    )
    order_history_id_set = set(
        MarketOrder.objects.filter(owner=character)
        .exclude(state=MarketOrder.StatusChoices.OPEN)
        .values_list("order_id", flat=True)
    )

    new_orders = [record for record in orders if record["order_id"] not in order_id_set]
    existing_orders = [
        record for record in orders if record["order_id"] in order_id_set
    ]

    create_new_orders(new_orders, character)
    if "history" in url:
        default_state = MarketOrder.StatusChoices.COMPLETED
        existing_active_orders = [
            record
            for record in existing_orders
            if record["order_id"] not in order_history_id_set
        ]
        update_existing_orders(existing_active_orders, default_state)
        logger.info(
            f"Updated {len(existing_active_orders)} history orders for {character.name}"
        )
    else:
        update_existing_orders(existing_orders)
        logger.info(f"Updated {len(existing_orders)} open orders for {character.name}")

    logger.info(f"Created {len(new_orders)} orders for {character.name}")


def create_new_orders(records: list, character: Character):
    new_orders = []
    for record in records:
        order = MarketOrder(
            order_id=record["order_id"],
            owner=character,
            location=Location.objects.get_or_create(eve_id=record["location_id"])[0],
            region=Region.objects.get_or_create(eve_id=record["region_id"])[0],
            article=Article.objects.get_or_create(eve_id=record["type_id"])[0],
            price=record["price"],
            volume_remain=record["volume_remain"],
            volume_total=record["volume_total"],
            issued=record["issued"],
            duration=record["duration"],
            range=record["range"],
            is_buy_order=record.get("is_buy_order", False),
            min_volume=record.get("min_volume", None),
            escrow=record.get("escrow", None),
            is_corporation=record.get("is_corporation", False)
            or record.get("is_corp", False),
        )
        order.state = (
            MarketOrder.StatusChoices.COMPLETED
            if record.get("volume_remain") == 0
            else record.get("state")
        )
        new_orders.append(order)
    MarketOrder.objects.bulk_create(new_orders)


def update_existing_orders(records: list, default_state=None):
    for record in records:
        try:
            order = MarketOrder.objects.get(order_id=record["order_id"])
            escrow = record.get("escrow", None)
            order.price = record["price"]
            order.volume_remain = record["volume_remain"]
            order.volume_total = record["volume_total"]
            order.issued = record.get("issued")
            if escrow is not None:
                order.escrow = escrow

            if default_state:
                order.state = (
                    default_state
                    if order.volume_remain == 0
                    else MarketOrder.StatusChoices(record.get("state", default_state))
                )

            order.save(
                update_fields=[
                    "price",
                    "volume_remain",
                    "volume_total",
                    "state",
                    "escrow",
                ]
            )
        except Exception as e:
            logger.error(e)


def update_character(auth: Auth, character: Character):
    location_data = fetch_data(
        auth,
        f"{auth.settings.data_url}/legacy/characters/{character.eve_id}/location/",
        character,
    )
    if location_data:
        character.location = SolarSystem.objects.get_or_create(
            eve_id=location_data["solar_system_id"]
        )[0]
    else:
        logger.error(f"{character.name} location not updated")

    sp_data = fetch_data(
        auth,
        f"{auth.settings.data_url}/v4/characters/{character.eve_id}/skills/",
        character,
    )
    if sp_data:
        character.total_sp = sp_data["total_sp"]
    else:
        logger.error(f"{character.name} SP not updated")

    character_data = fetch_data(
        auth,
        f"{auth.settings.data_url}/legacy/characters/{character.eve_id}/",
        character,
    )
    if character_data:
        update_corporation(character, character_data, auth)

    character.save(update_fields=["location", "total_sp", "corporation"])


def fetch_data(auth: Auth, url: str, character: Character) -> dict:
    data = auth.protected_access(url, character)
    if data is None or not len(data):
        logger.error(f"Failed to fetch data from {url}")
        return {}
    return data


def update_corporation(character: Character, character_data: dict, auth: Auth):
    if (
        character.corporation is None
        or character.corporation.eve_id != character_data["corporation_id"]
    ):
        corporation = Corporation.objects.get_or_create(
            eve_id=character_data["corporation_id"]
        )[0]

        corporation_data = fetch_data(
            auth,
            f'{auth.settings.data_url}/v5/corporations/{character_data["corporation_id"]}/',
            character,
        )
        corporation_icon_data = fetch_data(
            auth,
            f'{auth.settings.data_url}/v2/corporations/{character_data["corporation_id"]}/icons/',
            character,
        )

        corporation.name = corporation_data["name"]
        corporation.ticker = corporation_data["ticker"]
        corporation.icon = corporation_icon_data["px64x64"]

        corporation.save()
        character.corporation = corporation
