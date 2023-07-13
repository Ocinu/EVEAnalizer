import requests as rq
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from loguru import logger

from .auth import Auth
from .models import Character


class OverviewView(LoginRequiredMixin, ListView):
    model = Character
    template_name = "pilot/overview.html"
    context_object_name = "character_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = Auth()
        context["eve_login_url"] = auth.login_url
        context["total_balance"] = self.get_total_balance(
            context[self.context_object_name]
        )
        return context

    @staticmethod
    def get_total_balance(characters):
        return sum([character.wallet_balance for character in characters])


class CharacterView(UserPassesTestMixin, DetailView):
    model = Character
    template_name = "Pilot/character.html"

    def test_func(self):
        character = self.get_object()
        return self.request.user == character.owner

    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        open_orders = self.object.orders.filter(state="open").prefetch_related()
        closed_orders = self.object.orders.exclude(state="open").prefetch_related()

        context["active_shell"] = open_orders.filter(is_buy_order=False)
        context["active_buy"] = open_orders.filter(is_buy_order=True)
        context["history_shell"] = closed_orders.filter(is_buy_order=False)
        context["history_buy"] = closed_orders.filter(is_buy_order=True)
        return context


def callback(request):
    """Process callback data after a successful authentication on EVEasci. Save tokens and create new character"""

    auth = Auth()
    authorization_code = request.GET.get("code", "code error")
    tokens = auth.get_tokens(authorization_code)
    character_auth_data = auth.get_access(tokens)
    character_eve_id = character_auth_data["CharacterID"]
    if len(tokens):
        character = Character.objects.get_or_create(
            eve_id=character_auth_data["CharacterID"]
        )[0]
        character_data = rq.get(
            f"{auth.settings.data_url}/legacy/characters/{character_eve_id}/"
        ).json()
        portrait = rq.get(
            f"{auth.settings.data_url}/v2/characters/{character_eve_id}/portrait/"
        )
        character.owner = request.user

        character.name = character_data["name"]
        character.birthday = character_data["birthday"].split("T")[0]
        character.portrait = portrait.json()["px256x256"]
        character.refresh_token = tokens["refresh_token"]
        character.access_token = tokens["access_token"]
        character.save()
        logger.success("New character saved")
    else:
        logger.error("New character token not saved")
    return redirect(reverse("overview"))
