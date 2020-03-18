from app import Account, Trade, Position, ORM, controller, view
from app.util import get_price, hash_password

import os

DIR =  os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "data", "ttrader.db")
ORM.dbpath = DBPATH

controller.run()
'''
** Please run /data/schema.py first-- be sure you are in the data directory.
** Then, run the program here.-- be sure you are in the parent directory.
'''