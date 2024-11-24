from argparse import ArgumentParser
from os.path import exists
from typing import Set

from yaml import safe_load


class Parameters:

    DEFAULT_CONFIGURATION_PATH = './configuration/configuration.yml'

    @staticmethod
    def _load_config(config_path):
        """Loads the config file and returns the configuration dictionary."""
        if not exists(config_path):
            raise FileNotFoundError(f'Error: Config file not found: {config_path}!')

        with open(config_path, 'r') as file:
            return safe_load(file)

    @staticmethod
    def _generate_arguments_parser() -> ArgumentParser:
        """Generates the argument parser for the CLI."""
        parser = ArgumentParser(description='Generate Nintendo accounts')

        parser.add_argument('number_accounts', type=int, help='Number of accounts to generate')
        parser.add_argument('--username_length', type=int, help='Length of the generated username')
        parser.add_argument('--username_minimum_letters', type=int, help='Minimum number of letters for username')
        parser.add_argument('--username_minimum_digits', type=int, help='Minimum number of digits for username')
        parser.add_argument('--password_length', type=int, help='Length of the generated password')
        parser.add_argument('--forbidden_domains', nargs='*', help='List of forbidden domains for the emails')
        parser.add_argument('--maximum_workers', type=int, help='Maximum number of workers')
        parser.add_argument('--birthdate_lower', type=str, help='Lower bound for birthdate (YYYY-MM-DD)')
        parser.add_argument('--birthdate_upper', type=str, help='Upper bound for birthdate (YYYY-MM-DD)')
        parser.add_argument('--proxy_api_key', type=str, help='?')
        parser.add_argument('--timeout', type=int, help='?')
        parser.add_argument('--configuration', type=str, help='Path to the YAML config file', metavar='CONFIG')

        return parser

    @staticmethod
    def fetch_parameters():
        """Fetches parameters from command line args and config."""
        parser = Parameters._generate_arguments_parser()
        arguments = parser.parse_args()

        configuration_path = arguments.configuration or Parameters.DEFAULT_CONFIGURATION_PATH
        configuration = Parameters._load_config(configuration_path)

        number_accounts = arguments.number_accounts
        username_length = arguments.username_length if arguments.username_length is not None else configuration['USERNAME']['LENGTH']
        username_minimum_letters = arguments.username_minimum_letters if arguments.username_minimum_letters is not None else configuration['USERNAME'][
            'MINIMUM_LETTERS']
        username_minimum_digits = arguments.username_minimum_digits if arguments.username_minimum_digits is not None else configuration['USERNAME'][
            'MINIMUM_DIGITS']
        password_length = arguments.password_length if arguments.password_length is not None else configuration[
            'PASSWORD_LENGTH']
        forbidden_domains = set(
            arguments.forbidden_domains if arguments.forbidden_domains else configuration['FORBIDDEN_DOMAINS'])
        birthdate_lower = arguments.birthdate_lower if arguments.birthdate_lower else configuration['BIRTHDATE']['LOWER']
        birthdate_upper = arguments.birthdate_upper if arguments.birthdate_upper else configuration['BIRTHDATE']['UPPER']
        maximum_workers = arguments.maximum_workers if arguments.maximum_workers is not None else configuration['MAXIMUM_WORKERS']
        proxy_api_key = arguments.proxy_api_key if arguments.proxy_api_key is not None else configuration['PROXY_API_KEY']
        timeout = arguments.timeout if arguments.timeout is not None else configuration['TIMEOUT']

        return Parameters(
            number_accounts=number_accounts,
            username_length=username_length,
            username_minimum_letters=username_minimum_letters,
            username_minimum_digits=username_minimum_digits,
            password_length=password_length,
            forbidden_domains=forbidden_domains,
            birthdate_lower=birthdate_lower,
            birthdate_upper=birthdate_upper,
            maximum_workers=maximum_workers,
            proxy_api_key=proxy_api_key,
            timeout=timeout
        )

    def __init__(self,
                 number_accounts: int,
                 username_length: int,
                 username_minimum_letters: int,
                 username_minimum_digits: int,
                 forbidden_domains: Set[str],
                 password_length: int,
                 birthdate_lower: str,
                 birthdate_upper: str,
                 maximum_workers: int,
                 proxy_api_key: str,
                 timeout: int):
        self._number_accounts = number_accounts
        self._username_length = username_length
        self._username_minimum_letters = username_minimum_letters
        self._username_minimum_digits = username_minimum_digits
        self._forbidden_domains = forbidden_domains
        self._password_length = password_length
        self._birthdate_lower = birthdate_lower
        self._birthdate_upper = birthdate_upper
        self._maximum_workers = maximum_workers
        self._proxy_api_key = proxy_api_key
        self._timeout = timeout

    @property
    def number_accounts(self) -> int:
        return self._number_accounts

    @property
    def username_length(self) -> int:
        return self._username_length

    @property
    def username_minimum_letters(self) -> int:
        return self._username_minimum_letters

    @property
    def username_minimum_digits(self) -> int:
        return self._username_minimum_digits

    @property
    def forbidden_domains(self) -> Set[str]:
        return self._forbidden_domains

    @property
    def password_length(self) -> int:
        return self._password_length

    @property
    def birthdate_lower(self) -> str:
        return self._birthdate_lower

    @property
    def birthdate_upper(self) -> str:
        return self._birthdate_upper

    @property
    def maximum_workers(self) -> int:
        return self._maximum_workers

    @property
    def proxy_api_key(self) -> str:
        return self._proxy_api_key

    @property
    def timeout(self) -> int:
        return self._timeout
