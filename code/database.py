""" Connects to the Postgres database """
from copy import deepcopy
import json
import logging
import os

import daiquiri
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

class Database(object):
    """
    Connects to the Postgres database
    Connection settings appear in configuration.py
    Secrets must be stored in a .pgpass file
    """
    def __init__(self):
        # Configure the logger
        daiquiri.setup(level=logging.INFO)
        self.logger = daiquiri.getLogger(__name__)

        # Find the path to the file
        self.path = os.path.dirname(os.path.realpath(__file__))

        # Database connection and configurations
        self.columns = {}
        self.schema = 'open_source'
        self.database = 'postgres'
        self.connection = psycopg2.connect(user = 'postgres',
                                           dbname = 'postgres',
                                           host = 'localhost')

    def run_query(self, sql, commit=True):
        """ Runs a query against the postgres database """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        if commit:
            self.connection.commit()

    def load_item(self, item, table):
        """ Load items from a dictionary into a Postgres table """
        # Find the columns for the table
        if table not in self.columns:
            self.columns[table] = self.get_columns(table)
        columns = self.columns[table]

        # Determine which columns in the item are valid
        item_ = deepcopy(item)
        for key in item:
            if key not in columns:
                del item_[key]

        # Construct the insert statement
        n = len(item_)
        row = "(" + ', '.join(['%s' for i in range(n)]) + ")"
        cols = "(" + ', '.join([x for x in item_]) + ")"
        sql = """
            INSERT INTO {schema}.{table}
            {cols}
            VALUES
            {row}
        """.format(schema=self.schema, table=table, cols=cols, row=row)

        # Insert the data
        values = tuple([item_[x] for x in item_])
        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)
        self.connection.commit()
