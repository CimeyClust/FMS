import os
import sqlite3 as sql
import pandas as pd


class Model(object):
    def __init__(self):
        # Define connection and cursor
        self.connection = sql.connect('fms.db')
        self.cursor = self.connection.cursor()
        self.createTable()

        # Local AppData Directory --> self.connection = sql.connect(f'{os.getenv("LOCALAPPDATA")}\\fms.db')

    # Create the required tables for the program to work
    def createTable(self):
        # Creating SQL queries for the table generation
        table_benutzer = """ CREATE TABLE IF NOT EXISTS BENUTZER (
                             BenutzerID INTEGER PRIMARY KEY,
                             Vorname VARCHAR(255) NOT NULL,
                             Nachname VARCHAR(255) NOT NULL,
                             Klasse INTEGER(4) NULL DEFAULT NULL
                         ); """

        table_ausleihe = """ CREATE TABLE IF NOT EXISTS AUSLEIHE (
                             VorgangsID INTEGER PRIMARY KEY,
                             BenutzerID INTEGER UNSIGNED NOT NULL,
                             ExemplarID INTEGER UNSIGNED NOT NULL,
                             DatumEntleihe TIMESTAMP NULL DEFAULT NULL,
                             DatumRückgabe TIMESTAMP NULL DEFAULT NULL,
                             Bemerkung TEXT NOT NULL,
                             FOREIGN KEY (BenutzerID) REFERENCES `BENUTZER`(`BenutzerID`) ON DELETE CASCADE,
                             FOREIGN KEY (ExemplarID) REFERENCES `EXEMPLAR`(`ExemplarID`) ON DELETE CASCADE
                         ); """

        table_exemplar = """ CREATE TABLE IF NOT EXISTS EXEMPLAR (
                             ExemplarID INTEGER PRIMARY KEY,
                             TitelID INTEGER UNSIGNED NOT NULL,
                             Bemerkung TEXT NOT NULL,
                             FOREIGN KEY (TitelID) REFERENCES `TITEL`(`TitelID`) ON DELETE CASCADE
                         ); """

        table_titel = """ CREATE TABLE IF NOT EXISTS TITEL (
                          TitelID INTEGER PRIMARY KEY,
                          FachbereichsID INTEGER UNSIGNED NOT NULL,
                          Titel VARCHAR(255) NOT NULL,
                          ISBN INTEGER(13) NULL DEFAULT NULL,
                          Autor VARCHAR(255) NOT NULL,
                          FOREIGN KEY (FachbereichsID) REFERENCES `FACHBEREICH`(`FachbereichsID`) ON DELETE CASCADE
                      ); """

        table_fachbereich = """ CREATE TABLE IF NOT EXISTS FACHBEREICH (
                                FachbereichsID INTEGER PRIMARY KEY,
                                Fachbereichsname VARCHAR(255) NOT NULL
                            ); """

        # Execution of the SQL queries
        self.cursor.execute(table_benutzer)
        self.cursor.execute(table_ausleihe)
        self.cursor.execute(table_exemplar)
        self.cursor.execute(table_titel)
        self.cursor.execute(table_fachbereich)

    # Deletes the database
    def dumpDatabase(self):
        self.connection.close()
        os.remove("fms.db")

    # Deletes all tables
    def dumpTable(self, tables: list):
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Returns information about all tables in the database
    def tableInfo(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            table = pd.read_sql_query(f"SELECT * from {table_name}", self.connection)
            print(table_name+"\n", table, "\n")

    # Generell execute method for custom sql query
    def execute(self, query):
        self.cursor.execute(query)

    # Get Method for Tables
    def getTable(self, table_name: str, column: str):
        self.cursor.execute(f"SELECT {column} FROM {table_name};")
        return self.cursor.fetchall()

    # Insert methode for user
    def insertUser(self, name: str, surname: str, school_class: int):
        self.cursor.execute(f"INSERT INTO BENUTZER (Vorname, Nachname, Klasse) VALUES ('{name}','{surname}', {school_class});")

    # Get all IDs of the title entity
    def getTitleIDs(self):
        self.cursor.execute("SELECT TitelID FROM TITEL;")
        return self.cursor.fetchall()

    # Get the title of a Title entity by it's id
    def getTitleTitle(self, id: int):
        self.cursor.execute(f"SELECT Titel FROM TITEL WHERE TitelID = {id};")
        return self.cursor.fetchone()

    # Get the isbn of a Title entity by it's id
    def getTitleISBN(self, id: int):
        self.cursor.execute(f"SELECT ISBN FROM TITEL WHERE TitelID = {id};")
        return self.cursor.fetchone()

    # Get the author of a Title entity by it's id
    def getTitleAuthor(self, id: int):
        self.cursor.execute(f"SELECT Autor FROM TITEL WHERE TitelID = {id};")
        return self.cursor.fetchone()

    # Get the subject id of a Title entity by it's id
    def getTitleSubjectID(self, id: int):
        self.cursor.execute(f"SELECT FachbereichsID FROM TITEL WHERE TitelID = {id};")
        return self.cursor.fetchone()

    # Get all ids of the Fachwerk Entity
    def getSubjectIDs(self):
        self.cursor.execute("SELECT FachbereichsID FROM FACHBEREICH;")
        return self.cursor.fetchall()

    # Get the title of the subject by it's FachwerkID
    def getSubjectName(self, id: int):
        self.cursor.execute(f"SELECT Fachbereichsname FROM FACHBEREICH WHERE FachbereichsID = {id};")
        return self.cursor.fetchone()

    # Context Manager
    def __enter__(self):
        print("\nConnected to the database...\n")
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
        print("\nClosed connection to the database...")


if __name__ == "__main__":
    # Model().dumpDatabase()
    with Model() as db:
        db.insertUser("Yassin", "Starzetz", 1011)
        db.insertUser("Luis", "Hamann", 1011)
        db.insertUser("Leon", "Martin", 1011)
        db.insertUser("Jan", "Weinsheimer", 1011)
        db.tableInfo()
        db.dumpTable(['BENUTZER'])
