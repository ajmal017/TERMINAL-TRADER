import time
from .orm import ORM

class Trade(ORM):

    tablename = 'trades'
    fields =['accounts_pk', 'ticker', 'volume', 'price', 'time']
    #Filling class-speciic empty ORM fields. 

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.accounts_pk = kwargs.get('accounts_pk')
        self.ticker = kwargs.get('ticker')
        self.volume = kwargs.get('volume')
        self.price = kwargs.get('price')
        self.time = kwargs.get('time', time.time())

