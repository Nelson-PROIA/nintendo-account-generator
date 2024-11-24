from random import choice
from typing import List, Dict, Tuple, Any

from requests import get


class ProxyRotator:
    """TODO Comment"""

    PROXY_LIST_URL = 'https://proxy.webshare.io/api/v2/proxy/list/?mode=direct'

    def __init__(self, api_key: str):
        """TODO Comment"""
        self._api_key = api_key
        self._headers = {'Authorization': f'Token {self._api_key}'}

        self._proxies = self._fetch_all_proxies()
        self._last_proxy = None

    def _fetch_all_proxies(self) -> List[Dict[str, Any]]:
        """TODO Comment"""
        proxies = []
        url = ProxyRotator.PROXY_LIST_URL

        while url is not None:
            response = get(url, headers=self._headers)

            if response.status_code != 200:
                raise RuntimeError(f'Error: Failed to retrieve proxies, status code: {response.status_code}!')

            data = response.json()

            results = data.get('results', [])
            proxies.extend(self._parse_proxies(results))

            url = data.get('next')

        return proxies

    @staticmethod
    def _parse_proxies(results: List[Dict]) -> List[Dict[str, Any]]:
        """TODO Comment"""
        parsed_proxies = []

        for result in results:
            proxy = {
                'country': result.get('country_code'),
                'data': {
                    'address': result.get('proxy_address'),
                    'port': result.get('port'),
                    'username': result.get('username'),
                    'password': result.get('password')
                }
            }
            parsed_proxies.append(proxy)

        return parsed_proxies

    def get_next_proxy(self) -> Tuple[str, Dict[str, str]]:
        """TODO Comment"""
        available_proxies = [proxy for proxy in self._proxies if proxy != self._last_proxy]

        if not available_proxies:
            raise RuntimeError('Error: No proxies available!')

        next_proxy = choice(available_proxies)
        self._last_proxy = next_proxy

        return next_proxy['country'], next_proxy['data']
