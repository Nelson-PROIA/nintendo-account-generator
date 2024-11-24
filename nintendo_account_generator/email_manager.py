from random import choice
from re import search
from typing import Set, Optional

from requests import get


class EmailManager:

    DOMAIN_ENDPOINT = "https://www.1secmail.com/api/v1/?action=getDomainList"

    GET_MESSAGES_ENDPOINT = "https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    READ_MESSAGE_ENDPOINT = "https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}"

    @staticmethod
    def get_verification_code(email: str) -> Optional[str]:
        login, domain = email.split('@')

        messages_url = EmailManager.GET_MESSAGES_ENDPOINT.format(login=login, domain=domain)
        response = get(messages_url)

        if response.status_code != 200:
            raise RuntimeError(f'Error: Failed to retrieve messages, status code: {response.status_code}!')

        messages = response.json()
        verification_id = None

        for message in messages:
            if message.get('subject', '').endswith('Nintendo Account: E-mail address verification'):
                verification_id = message['id']
                break

        if verification_id is None:
            return None

        read_message_url = EmailManager.READ_MESSAGE_ENDPOINT.format(login=login, domain=domain,
                                                                     message_id=verification_id)
        response = get(read_message_url)

        if response.status_code != 200:
            raise RuntimeError(f'Failed to read the message, status code: {response.status_code}!')

        message_body = response.json().get('body', '')
        match = search(r'Verification code:\n(\d{4})', message_body)

        if match:
            return match.group(1)
        else:
            raise RuntimeError('Error: Verification code not found!')

    def __init__(self, forbidden_domains: Set[str]):
        self._forbidden_domains = forbidden_domains

    def generate_email(self, username: str) -> str:
        response = get(EmailManager.DOMAIN_ENDPOINT)

        if response.status_code != 200:
            raise RuntimeError('Error: Domains could not be fetched!')

        domains = response.json()
        available_domains = [domain for domain in domains if domain not in self._forbidden_domains]

        if not available_domains:
            raise RuntimeError('Error: No available domains found!')

        domain = choice(available_domains)

        return f'{username}@{domain}'
