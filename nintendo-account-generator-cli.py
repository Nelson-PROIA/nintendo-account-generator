from nintendo_account_generator.accounts_generator import AccountsGenerator
from nintendo_account_generator.parameters import Parameters


if __name__ == '__main__':
    parameters = Parameters.fetch_parameters()
    accounts_generator = AccountsGenerator(parameters)

    accounts = accounts_generator.generate_accounts()

    for account in accounts:
        print(account)
