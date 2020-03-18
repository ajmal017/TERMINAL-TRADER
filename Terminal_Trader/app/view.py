import colorama

'''
View functions-- all print/success/error messages in 
program come from here.
'''

def option_select():
    return input("\nPlease select one of the following options. ")

def main_menu():
    print("\n{}STONK${}".format(colorama.Fore.GREEN, colorama.Fore.RESET))
    print(f"{colorama.Fore.GREEN}Welcome to terminal trader!{colorama.Fore.RESET}")
    print("1). Create account")
    print("2). Log in")
    print("3). Quit")

def print_logged_in():
    print("""
    1). See Balance & Positions
    2). Deposit money
    3). Look up stock price
    4). Buy stock
    5). Sell stock
    6). Trade history
    7). Log out""")

def not_valid_option():
    print(f"\n{colorama.Fore.RED}You did not select a valid option! Please try again.{colorama.Fore.RESET}")

def create_account_prompt():
    return input(f"{colorama.Fore.BLUE}Thank you for choosing to create an account!\nPlease enter your username: {colorama.Fore.RESET}")

def account_already_exists(name):
    print(f"\n{colorama.Fore.RED}Account {name} already exists in our database. Please try another username or log in.{colorama.Fore.RESET}\n")

def log_in_prompt():
    return input(f"{colorama.Fore.BLUE}Welcome back!\nPlease enter your username: {colorama.Fore.RESET}")

def account_found(account):
    print(f"\n{colorama.Fore.GREEN}Account found! Welcome, {account.username}.{colorama.Fore.RESET}\n")

def print_balance(balance):
    print(f"\n{colorama.Fore.GREEN}Your current account balance is: ${balance}{colorama.Fore.RESET}.")

def add_balance():
    return input(f"{colorama.Fore.BLUE}Please enter a desired amount to add: {colorama.Fore.RESET}")

def balance_success(balance):
    print(f"\n{colorama.Fore.GREEN}You have successfully deposited: ${balance}{colorama.Fore.RESET}.")

def negative_balance_prompt():
    print(f"\n{colorama.Fore.RED}You are not allowed to deposit a negative balance.{colorama.Fore.RESET}")

def request_ticker():
    return input("Please enter the company's ticker: ")

def print_ticker_price(ticker,price):
    print(f"{colorama.Fore.GREEN}\nThe current price of {ticker.upper()} is ${str(price)}.{colorama.Fore.RESET}")

def not_valid_ticker():
    print(f"\n{colorama.Fore.RED}This is not a valid ticker!{colorama.Fore.RESET}")

def request_buy():
    return input("Please enter the amount of shares you would like to purchase: ")

def buy_success(amount,ticker):
    print(f"\n{colorama.Fore.GREEN}You have purchased {str(amount)} shares of {ticker.upper()}{colorama.Fore.RESET}.")

def request_sell():
    return input("Please enter the amount of shares you would like to sell: ")

def sell_sucess(amount,ticker):
    print(f"\n{colorama.Fore.GREEN}You have sold {str(amount)} shares of {ticker.upper()}{colorama.Fore.RESET}.")

def not_enough_shares():
    print(f"\n{colorama.Fore.RED}You do not have enough shares in this account to sell.{colorama.Fore.RESET}")    

def no_stock_owned(ticker):
    print(f"\n{colorama.Fore.RED}You do not own stock in {ticker.upper()}.{colorama.Fore.RESET}") 

def account_not_found():
    print("\nAccount not found. Please try again.\n")

def password_prompt():
    return input(f"{colorama.Fore.BLUE}Please enter your password: {colorama.Fore.RESET}")

def balance_prompt():
    return input(f"{colorama.Fore.BLUE}Please input your starting balance: {colorama.Fore.RESET}")

def print_positions(positions):
    for position in positions:
        print(f"{colorama.Fore.GREEN}You have {position.shares} shares of {position.ticker.upper()}{colorama.Fore.RESET}.")

def print_trades(trades):
    if trades==[]:
        print(f"\n{colorama.Fore.RED}This account has no trade history!{colorama.Fore.RESET}") 
    else:
        for trade in trades:
            print(f"\n{colorama.Fore.GREEN}Account number: {trade.accounts_pk} - Ticker:{trade.ticker.upper()} - Volume: {trade.volume} At Price: ${trade.price}{colorama.Fore.RESET}.")

def exit_message():
    print(f"{colorama.Fore.RED}\n***\nThank you for using Terminal Trader-- Goodbye!\n***\n{colorama.Fore.RESET}")
