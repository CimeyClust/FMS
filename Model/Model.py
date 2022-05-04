import os
import sqlite3
import pandas as pd


class Model(object):
    def __init__(self):
        # Define connection and cursor
        self.connection = sqlite3.connect('fms.db')
        self.cursor = self.connection.cursor()

    def createTable(self):
        with self:
            # Creating SQL commands for the table generation
            table_benutzer = """ CREATE TABLE IF NOT EXISTS BENUTZER (
                                 BenutzerID INTEGER PRIMARY KEY AUTOINCREMENT,
                                 Vorname VARCHAR(255) NOT NULL,
                                 Nachname VARCHAR(255) NOT NULL,
                                 Klasse INTEGER(4) NULL DEFAULT NULL
                             ); """

            table_entleiht = """ CREATE TABLE IF NOT EXISTS ENTLEIHT (
                                 VorgangsID INTEGER PRIMARY KEY AUTOINCREMENT,
                                 BenutzerID INTEGER UNSIGNED NOT NULL,
                                 ExemplarID INTEGER UNSIGNED NOT NULL,
                                 DatumEntleihe TIMESTAMP NOT NULL,
                                 DatumRückgabe TIMESTAMP NOT NULL,
                                 FOREIGN KEY (BenutzerID) REFERENCES `BENUTZER`(`BenutzerID`) ON DELETE CASCADE,
                                 FOREIGN KEY (ExemplarID) REFERENCES `EXEMPLAR`(`ExemplarID`) ON DELETE CASCADE
                             ); """

            table_exemplar = """ CREATE TABLE IF NOT EXISTS EXEMPLAR (
                                 ExemplarID INTEGER PRIMARY KEY AUTOINCREMENT,
                                 TitelID INTEGER UNSIGNED NOT NULL,
                                 Bemerkung VARCHAR(255) NOT NULL,
                                 FOREIGN KEY (TitelID) REFERENCES `TITEL`(`TitelID`) ON DELETE CASCADE
                             ); """

            table_titel = """ CREATE TABLE IF NOT EXISTS TITEL (
                              TitelID INTEGER PRIMARY KEY AUTOINCREMENT,
                              FachbereichsID INTEGER UNSIGNED NOT NULL,
                              Titel VARCHAR(255) NOT NULL,
                              ISBN INTEGER(13) NULL DEFAULT NULL,
                              Autor VARCHAR(255) NOT NULL,
                              FOREIGN KEY (FachbereichsID) REFERENCES `FACHBEREICH`(`FachbereichsID`) ON DELETE CASCADE
                          ); """

            table_fachbereich = """ CREATE TABLE IF NOT EXISTS FACHBEREICH (
                                    FachbereichsID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Fachbereichsname VARCHAR(255) NOT NULL
                                ); """

            # Execution of the SQL commands
            self.cursor.execute(table_benutzer)
            self.cursor.execute(table_entleiht)
            self.cursor.execute(table_exemplar)
            self.cursor.execute(table_titel)
            self.cursor.execute(table_fachbereich)

    # Deletes all tables
    def dumpTables(self):
        with self:
            self.cursor.execute("DROP TABLE IF EXISTS BENUTZER")
            self.cursor.execute("DROP TABLE IF EXISTS ENTLEIHT")
            self.cursor.execute("DROP TABLE IF EXISTS EXEMPLAR")
            self.cursor.execute("DROP TABLE IF EXISTS TITEL")
            self.cursor.execute("DROP TABLE IF EXISTS FACHBEREICH")

    # Returns information about all tables in the database
    def tableInfo(self):
        with self:
            tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            for table_name in tables:
                table_name = table_name[0]  # tables is a list of single item tuples
                table = pd.read_sql_query("SELECT * from {} LIMIT 0".format(table_name), self.connection)
                print(table_name)
                for col in table.columns:
                    print('\t' + col)
                print()

    # Quick insert methode for testing wil get improved later on
    def insert(self):
        with self:
            yadel = "INSERT INTO BENUTZER (Vorname, Nachname, Klasse) VALUES ('Yassin','Starzetz', 1011);"
            mrnoodle = "INSERT INTO BENUTZER (Vorname, Nachname, Klasse) VALUES ('Vincent','Starzetz', 1011);"

            self.cursor.execute(yadel)
            self.cursor.execute(mrnoodle)

    # Quick getter methode for the User table, will get improved later
    def getUser(self):
        with self:
            self.cursor.execute("SELECT * FROM BENUTZER;")
            print(self.cursor.fetchall())

    # Context Manager
    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


if __name__ == "__main__":

    Model().createTable()
    Model().tableInfo()
    Model().insert()
    Model().getUser()

# ignore this for the moment
os.getenv('LOCALAPPDATA')
