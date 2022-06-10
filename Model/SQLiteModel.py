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
                             Password VARCHAR(255) NOT NULL,
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

    #######################################################################
    #
    #  Function to generate a QR-Code as image out of a number.
    #
    #  This function is used to convert the book id into a qr-code
    #  and save it locally as image
    #
    #  @param id: A number that represents a Book ID
    #
    #######################################################################

    def generateQRCode(self, id: int):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(id)
        qr.make(fit=True)

        path = tkinter.filedialog.askdirectory(initialdir=os.path.expanduser("~"))

        img = qr.make_image(fill_color="black", back_color="white")
        # img.save(os.getcwd() + "\\Book" + str(id) + ".png")
        try:
            os.mkdir(path + "\\Books")
        except OSError:
            pass
        img.save(path + "\\Books\\Book" + str(id) + ".png")

    def getConnectionHost(self, id: int):
        self.cursor.execute(f"SELECT Host FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def getConnectionUser(self, id: int):
        self.cursor.execute(f"SELECT User FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def getConnectionPassword(self, id: int):
        self.cursor.execute(f"SELECT Password FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def getConnectionDatabase(self, id: int):
        self.cursor.execute(f"SELECT Database FROM `CONNECTION` WHERE ConnectionID = {id}")
        return self.cursor.fetchone()

    def updateConnection(self, id: int, host: str, user: str, password: str, database: str):
        statement = f"UPDATE CONNECTION SET Host = '{host}', User = '{user}', Password = '{password}', Database = '{database}' WHERE ConnectionID = {id};"
        self.cursor.execute(statement)

    def insertEmptyConnection(self, id):
        statement = f"INSERT INTO CONNECTION (ConnectionID, Host, User, Password, Database) VALUES({id}, '', '', '', '');"
        self.cursor.execute(statement)
