import sqlite3
from _ast import arg
from os import path, getcwd

from wheel.signatures.djbec import q

db = path.join(getcwd(), 'database.db')


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(db)

    def query(self, q, arg=()):
        cursor = self.connection.cursor()

        cursor.execute(q, arg)
        results = cursor.fetchall()
        cursor.close()

        return results

    def insert(self, q, arg=()):
        cursor = self.connection.cursor()

        cursor.execute(q, arg)
        self.connection.commit()
        result = cursor.lastrowid
        cursor.close()

        return result

    def select(self, q, args=()):
        cursor = self.connection.cursor()

        return cursor.execute(q, args)

    def delete(self):
        cursor = self.connection.cursor()

        result = cursor.execute(q, arg)
        self.connection.commit()
        cursor.close()

        return result
