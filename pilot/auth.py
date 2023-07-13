import json
from typing import Optional

import requests

from core.logger import logger
from main.models import Settings
from pilot.models import Character
from pilot.scopes import SCOPES


class Auth:
    def __init__(self):
        self.settings = Settings.objects.get(is_active=True)
        self.session = requests.Session()
        self.base_url = f"{self.settings.base_url}/oauth/token"
        self.verify_url = f"{self.settings.base_url}/oauth/verify"
        self.login_url = (
            f"{self.settings.base_url}/oauth/authorize?"
            f"response_type={self.settings.response_type}&"
            f"redirect_uri={self.settings.redirect_url}&"
            f"client_id={self.settings.client_id}&"
            f"scope={SCOPES}"
        )

    def _get_json_response(self, response) -> Optional[dict]:
        if response.status_code != 200:
            logger.error(f"Request failed with status code: {response.status_code}")
            return None
        return response.json()

    def _make_request(
        self, method: str, url: str, headers=None, data=None
    ) -> Optional[dict]:
        try:
            response = self.session.request(method, url, headers=headers, data=data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        else:
            return self._get_json_response(response)

    def get_tokens(self, authorization_code: str) -> dict:
        base_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.settings.base64_key}",
        }
        base_data = {"grant_type": "authorization_code", "code": authorization_code}
        response = self._make_request(
            "POST",
            self.base_url,
            headers=base_headers,
            data=json.dumps(base_data, indent=4),
        )
        return response if response else {}

    def get_access(self, tokens: dict) -> dict:
        verify_header = {"Authorization": f"Bearer {tokens.get('access_token')}"}
        response = self._make_request("GET", self.verify_url, headers=verify_header)
        if not response:
            return self.refresh_access_token(tokens)
        return response

    def refresh_access_token(self, tokens: dict) -> dict:
        update_header = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.settings.base64_key}",
        }
        update_body = {
            "grant_type": "refresh_token",
            "refresh_token": tokens.get("refresh_token"),
        }
        response = self._make_request(
            "POST",
            self.base_url,
            headers=update_header,
            data=json.dumps(update_body, indent=4),
        )
        logger.info(f"Refresh access token response: {self.base_url}, {response}")
        if response:
            tokens["access_token"] = response.get("access_token")
            tokens["refresh_token"] = response.get("refresh_token")
            logger.info("Refresh access token successfully")
        return tokens if response else {}

    def protected_access(self, url: str, character: Character):
        tokens = {
            "access_token": character.access_token,
            "refresh_token": character.refresh_token,
        }
        protected_headers = {"Authorization": f"Bearer {tokens.get('access_token')}"}
        response = self._make_request("GET", url, headers=protected_headers)
        if not response:
            tokens = self.refresh_access_token(tokens)
            if tokens.get("access_token") and tokens.get("refresh_token"):
                character.access_token = tokens["access_token"]
                character.refresh_token = tokens["refresh_token"]
                character.save(update_fields=["access_token", "refresh_token"])

                protected_headers = {
                    "Authorization": f"Bearer {tokens['access_token']}"
                }
                response = self._make_request("GET", url, headers=protected_headers)
        return response if response else {}

    def get_rq(self, url: str) -> dict:
        response = self._make_request("GET", url)
        return response if response else {}
