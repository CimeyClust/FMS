###########################################################################
#
# SQLiteModel.py
# Program made by Luis and Yassin for the FMS project.
#
###########################################################################

import sqlite3 as sql
import tkinter.filedialog

import pandas as pd
import datetime
import os
import qrcode


###########################################################################
#
#    The Database class of the FMS.
#
#    [what this class does]
#
###########################################################################

class SQLiteModel(object):

    #######################################################################
    #
    #  The constructor of the Database class.
    #
    #  Defines the connection and cursor of the database.
    #  It calls the createTable() method which generates all tables if they
    #  haven't already.
    #
    #  @see createTable()
    #
    #######################################################################

    def __init__(self):
        # self.connection = sql.connect(os.getcwd() + '\\fms.db')
        try:
            os.mkdir(f'{os.getenv("LOCALAPPDATA")}\\FMS')
        except OSError:
            pass
        self.connection = sql.connect(f'{os.getenv("LOCALAPPDATA")}\\FMS\\fms.db')
        self.cursor = self.connection.cursor()
        # self.createTable()
        self.createConnectionTable()

        # Local AppData Directory --> self.connection = sql.connect(f'{os.getenv("LOCALAPPDATA")}\\fms.db')

    #######################################################################
    #
    #  Function to create tables.
    #
    #  This function builds the necessary tables for the FMS in order to
    #  work properly.
    #
    #######################################################################

    def createConnectionTable(self):
        table_connection = """ CREATE TABLE IF NOT EXISTS CONNECTION (
                             ConnectionID INTEGER PRIMARY KEY,
                             Host VARCHAR(255) NOT NULL,
                             User VARCHAR(255) NOT NULL,
                             Database VARCHAR(255) NOT NULL
                         ); """
        self.cursor.execute(table_connection)

    #######################################################################
    #
    #  Function to open and close a database connection.
    #
    #  By managing the database connection as a context manager, the Database
    #  can be opened as a context method, using a 'with ... as' statement.
    #
    #######################################################################

    def __enter__(self):
        # ("\nConnected to the database...\n")
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        # if an error occurs any changes to the database since the last call to commit() will get rolled back
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
        # print("\nClosed connection to the database...")

    def getConnectionHost(self, id: int):
        self.cursor.execute(f"SELECT Host FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def getConnectionUser(self, id: int):
        self.cursor.execute(f"SELECT User FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def getConnectionDatabase(self, id: int):
        self.cursor.execute(f"SELECT Database FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def updateConnection(self, id: int, host: str, user: str, database: str):
        statement = f"UPDATE CONNECTION SET Host = '{host}', User = '{user}', Database = '{database}' WHERE ConnectionID = {id};"
        self.cursor.execute(statement)

    def insertEmptyConnection(self, id):
        statement = f"INSERT INTO CONNECTION (ConnectionID, Host, User, Password, Database) VALUES({id}, " \
                    f"'', '', '', '');"
        self.cursor.execute(statement)
