import os
import json
from .account import Account
from .position import Position
from .trade import Trade
from .orm import ORM
from .view import * 
from .util import *

def logged_in(account):
    #Only executes when account object is found in DB. 
    while True:
        print_logged_in()
        #Prints menu of authenticated user options. 
        choice=option_select()
        if choice=="1":
        #Prints list of positions and user's balance.
            position_list=account.get_positions()   
            print_balance(account.balance)
            print_positions(position_list)
        elif choice=="2":
        #Deposit balance into account & update database.
            amount=add_balance()
            if int(amount)>0:
                account.balance+=round(float(amount),2)
                balance_success(amount)
                account.save()
            else:
            #Error handling: Inputting negative baalnce
                negative_balance_prompt()
        elif choice=="3":
        #Print current market value of inputter ticker. 
            try:
                ticker=request_ticker()
                price=get_price(ticker)
                print_ticker_price(ticker,price)
            except:
            #Error handling: Invalid ticker name (Company does not exist)
                not_valid_ticker()
        elif choice=="4":
        #Purchase shares of desired ticker-- fetches current value from API.
            try:
                ticker=request_ticker()
                amount=request_buy()
                account.buy(ticker,int(amount))
                buy_success(amount,ticker)
            except json.decoder.JSONDecodeError:
            #Error handling: Invalid ticker name (Company does not exist)
                not_valid_ticker()
        elif choice=="5":
        #Sell shares of desired ticker-- fetches current value from API.
            try:
                ticker=request_ticker()
                amount=request_sell()
                account.sell(ticker,int(amount))
                sell_sucess(amount,ticker)
            except json.decoder.JSONDecodeError:
            #Error handling: Invalid ticker name (Company does not exist)
                not_valid_ticker()
            except ValueError:
            #Error handling: Attempting sale of more shares than you own.
                not_enough_shares()
            except AttributeError:
            #Error handling: Do not currently have positions with this ticker.
                no_stock_owned(ticker)
        elif choice=="6":
            trade_list=account.get_trades()
            print_trades(trade_list)
        elif choice=="7":
            #Quit program.
            exit_message()
            break
        else:
            not_valid_option()
        
def run():  
    while True:
        main_menu()
        choice=option_select()
        if choice=="1":
            #Create account option-- unique usernames only.
            try:
                username=create_account_prompt()
                password=password_prompt()
                hashed_password=hash_password(password)
                #Hashes password before entering it into DB. 
                balance=int(balance_prompt())
                new_acc=Account(username=username,password_hash=hashed_password,balance=balance)
                new_acc.save()
            except:
            #Error handling: account already exists in DB. 
                account_already_exists(username)
        elif choice=="2":
            #Log in option-- fetches account object and throws error when not in DB.
            username=log_in_prompt()
            password=password_prompt()
            account_success=Account.login(username=username,password=password)
            #Returns account object if found -- None if not. 
            if account_success==None:
                account_not_found()
            else:
                account_found(account_success)
                logged_in(account_success)
        elif choice=="3":
            #Quit program. Break true loop. 
            exit_message()
            break
        else:
            not_valid_option()

