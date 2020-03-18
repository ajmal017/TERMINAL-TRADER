import sqlite3
import os
from app import Account
from unittest import TestCase
from data import schema
from app import hash_password
# python3 -m unittest discover tests

DIR = os.path.dirname(__file__)
DBFILENAME = "test.db"
DBPATH = os.path.join(DIR, DBFILENAME)

Account.dbpath = DBPATH

class testAccount(TestCase):

    def setUp(self):
        schema(DBPATH)

    def tearDown(self):
        os.remove(DBPATH)

    def test_select_one_by_pk(self):
        new_acc = Account(username="dan.m",password_hash="1234",balance=10000)
        new_acc.save()
        item = Account.one_from_pk(1)
        self.assertEqual(item.username, "dan.m")
        self.assertEqual(item.balance, 10000)
    
    def test_password_hash(self):
        hashed_pass = hash_password("1234")
        new_acc = Account(username="dan.m",password_hash=hashed_pass,balance=10000)
        new_acc.save()
        item = Account.one_from_pk(1)
        self.assertEqual(item.password_hash, hashed_pass)
    
    def test_select_all(self):
        new_acc = Account(username="dan.m",password_hash="1234",balance=10000)
        new_acc2 = Account(username="tom.m",password_hash="4321",balance=20000)
        new_acc.save()
        new_acc2.save()
        acc_list = Account.all_from_where_clause()
        self.assertEqual(len(acc_list), 2)

    def test_update(self):
        new_acc = Account(username="dan.m",password_hash="1234",balance=10000)
        new_acc2 = Account(username="tom.m",password_hash="4321",balance=20000)
        new_acc.save()
        new_acc2.save()
        new_acc.username = "test"
        new_acc2.username = "test2"
        new_acc.save()
        new_acc2.save()
        item1 = Account.one_from_pk(1)
        item2 = Account.one_from_pk(2)
        self.assertEqual(item1.username, "test")
        self.assertEqual(item2.username, "test2")
    
    # def test_unique_username_create():
    #     new_acc = Account(username="dan.m",password_hash="1234",balance=10000)
    #     new_acc2 = Account(username="dan.m",password_hash="1234",balance=10000)
    #     new_acc.save()
    #     new_acc2.save()
    #     self.assertRaises(sqlite3.IntegrityError, new_acc2.username)
    
    # def test_unique_username_failure(self):
    #     with self.assertRaises(sqlite3.IntegrityError): test_unique_username_create()

