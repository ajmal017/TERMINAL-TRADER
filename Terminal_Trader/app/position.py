from .orm import ORM
from .util import get_price

class Position(ORM):

    tablename = 'positions'
    fields = ['accounts_pk', 'ticker', 'shares']
    #Filling class-speciic empty ORM fields. 

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.accounts_pk = kwargs.get('accounts_pk')
        self.ticker = kwargs.get('ticker')
        self.shares = kwargs.get('shares')

