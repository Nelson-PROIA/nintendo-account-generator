from json import load
from time import time, sleep
from typing import Tuple

import seleniumwire.undetected_chromedriver as uc

from nintendo_account_generator.email_manager import EmailManager
from nintendo_account_generator.form_submitter import FormSubmitter
from nintendo_account_generator.proxies import ProxyRotator
from nintendo_account_generator.utils import generate_username, generate_password, generate_birthdate


class AccountsGenerator:

    NINTENDO_ACCOUNT_REGISTRATION_URL = 'https://accounts.nintendo.com/register'

    REGISTER_FORM_PATH = './configuration/forms/register.json'
    CONFIRM_REGISTRATION_FORM_PATH = './configuration/forms/confirm-registration.json'
    VERIFY_EMAIL_FORM_PATH = './configuration/forms/verify-email.json'

    def __init__(self, parameters, proxy_rotation: bool = True, humanize: bool = True):
        self._parameters = parameters
        self._humanize = humanize

        self._proxy_rotator = ProxyRotator(self._parameters.proxy_api_key) if proxy_rotation else None
        self._email_manager = EmailManager(self._parameters.forbidden_domains)

        self._register_submitter = None
        self._confirm_registration_submitter = None
        self._verify_email_submitter = None

    def generate_accounts(self):
        total = 0

        for _ in range(self._parameters.number_accounts):
            self._generate_account()
            total += 1

        print('Total:', total)

    def _generate_account(self):
        country, driver = self._get_driver()
        driver.get(AccountsGenerator.NINTENDO_ACCOUNT_REGISTRATION_URL)

        self._set_submitters(country)

        account = self._register(driver)
        sleep(1000)
        self._confirm_registration(driver)
        self._verify_email(driver, account.get('email'))

        return account

    def _get_driver(self) -> Tuple[str, uc.Chrome]:
        options = uc.ChromeOptions()

        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("start-maximized")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--incognito")

        if self._proxy_rotator:
            country, proxy = self._proxy_rotator.get_next_proxy()
            proxy_server = f'{proxy.get('address')}:{proxy.get('port')}'

            proxy_options = {
                'proxy': {
                    'http': f'http://{proxy.get('username')}:{proxy.get('password')}@{proxy_server}',
                    'https': f'http://{proxy.get('username')}:{proxy.get('password')}@{proxy_server}',
                    'no_proxy': 'localhost,127.0.0.1',
                }
            }

            return country, uc.Chrome(options=options, seleniumwire_options=proxy_options)

        return 'FR', uc.Chrome(options=options)

    def _set_submitters(self, country: str) -> None:
        self._register_submitter = self._get_submitter(country, AccountsGenerator.REGISTER_FORM_PATH)
        self._confirm_registration_submitter = self._get_submitter(country, AccountsGenerator.CONFIRM_REGISTRATION_FORM_PATH)
        self._verify_email_submitter = self._get_submitter(country, AccountsGenerator.VERIFY_EMAIL_FORM_PATH)

    def _get_submitter(self, country: str, forms_path: str) -> FormSubmitter:
        with open(forms_path, 'r') as file:
            forms = load(file)

        for form in forms:
            associated_countries = form.get('associated_countries', 'ALL')

            if ((isinstance(associated_countries, str) and associated_countries == 'ALL') or
                    (isinstance(associated_countries, list) and country in associated_countries)):
                return FormSubmitter(form.get('inputs', {}), self._humanize)

        raise RuntimeError(f'Error: Country \'{country}\' not found in the associated countries of form at {forms_path}!')


    def _register(self, driver):
        username = generate_username(self._parameters.username_length, self._parameters.username_minimum_letters,
                                     self._parameters.username_minimum_digits)
        email = self._email_manager.generate_email(username)
        password = generate_password(self._parameters.password_length)
        birthdate = generate_birthdate(self._parameters.birthdate_lower, self._parameters.birthdate_upper)
        birth_year, birth_month, birth_day = [value.lstrip('0') for value in birthdate.split('-')]

        data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password,
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day,
            'gender': None,
            'country': None,
            'terms_consented': True,
            'policy_consented': True
        }

        self._register_submitter.submit_form(driver, data)

        return {
            'username': username,
            'email': email,
            'password': password
        }

    def _confirm_registration(self, driver):
        data = {
            'email_opted_in_unreceive': True
        }

        self._confirm_registration_submitter.submit_form(driver, data)

    def _verify_email(self, driver, email: str):
        verification_code = self._get_verification_code(email)

        data = {
            'verification_code': verification_code
        }

        self._verify_email_submitter.submit_form(driver, data)

    def _get_verification_code(self, email: str) -> str:
        start_time = time()

        while True:
            if time() - start_time > self._parameters.TIMEOUT:
                raise RuntimeError('Error: Timeout reached, verification code not found!')

            verification_code = EmailManager.get_verification_code(email)

            if verification_code:
                return verification_code

            sleep(1)
