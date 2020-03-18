import sqlite3
from .orm import ORM
from .position import Position
from .trade import Trade
from .util import hash_password,get_price
from .view import *

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance"]
    #Filling class-speciic empty ORM fields. 

    def __init__(self, **kwargs):
        #Constructor-- sets account username, balance, password and desired initial balance. 
        self.pk = kwargs.get('pk')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.balance = kwargs.get('balance')

    @classmethod
    def login(cls, username, password):
        # Will return an Account instance if successful.
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            sql = """SELECT * FROM accounts WHERE username=? AND password_hash=?;"""
            cursor.execute(sql, (username, hash_password(password)))
            user = cursor.fetchone()
            if user:
                return cls(**user)
            return None

    def get_position(self, ticker):
        # Returns a postiion instance corresponding to this user's postiion for this ticker.
        # SELECT * FROM positions WHERE account_pk=self.pk AND ticker=ticker;
        sql = "WHERE accounts_pk=? AND ticker=?;"
        return Position.one_from_where_clause(sql, values=(self.pk, ticker))

    def get_positions(self):
        # Returns all position instances corresponding to this user.
        sql = "WHERE accounts_pk=? AND shares>0;"
        return Position.all_from_where_clause(sql, values=(self.pk,))

    def get_trades(self):
        # Returns all trade instances corresponding to this user.
        sql = "WHERE accounts_pk=?;"
        return Trade.all_from_where_clause(sql, values=(self.pk,))

    def buy(self, ticker, amount):
        transaction_price = get_price(ticker) * amount
        #Fetches price from API and * by desired shares-- calculates total cost of investment. 
        if self.balance < transaction_price:
            raise ValueError("Balance is is too low")
        #Error handling: transaction cost>current balance
        self.balance -= transaction_price
        #Decrease accout balance
        new_trade = Trade(accounts_pk=self.pk,ticker=ticker,volume=amount,price=transaction_price)
        new_trade.save()
        #Create new trade instance & saves to DB.
        current = self.get_position(ticker)
        if current == None:
            current = Position(accounts_pk=self.pk,ticker=ticker,shares=0)
            current.save()
        current.shares += amount
        current.save()
        #Creates new position instance if one does not exist and increases its shares attribute. 
        self.save()

    def sell(self, ticker, amount):
        transaction_price = get_price(ticker) * amount
        #Fetches price from API and * by desired shares-- calculates total cost of investment. 
        position = self.get_position(ticker)
        if position.shares < amount:
            raise ValueError("Not enough shares.")
            # not_enough_shares()
        #Error handling: attempting to sell more shares than you own. 
        #TODO TEST THIS 
        self.balance += transaction_price
        self.save()
        new_trade = Trade(accounts_pk=self.pk,ticker=ticker,volume=amount,price=transaction_price)
        new_trade.save()
        #Creates new trade instance & saves to DB. 
        current = self.get_position(ticker)
        current.shares -= amount
        current.save()
        #Decreases position shares attributes & updates DB.
        self.save()