import os
import sqlite3
import pandas as pd


class Model:
    def __init__(self):

        # define connection and cursor
        connection = sqlite3.connect('fms.db')
        cursor = connection.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS BENUTZER")
        cursor.execute("DROP TABLE IF EXISTS EXEMPLAR")
        cursor.execute("DROP TABLE IF EXISTS TITEL")
        cursor.execute("DROP TABLE IF EXISTS FACHBEREICH")

        # Creating table
        table_benutzer = """ CREATE TABLE BENUTZER (
                             BenutzerID INTEGER PRIMARY KEY AUTOINCREMENT,
                             Vorname VARCHAR(255) NOT NULL,
                             Nachname VARCHAR(255) NOT NULL,
                             Klasse INT(4) NULL DEFAULT NULL
                         ); """

        table_exemplar = """ CREATE TABLE EXEMPLAR (
                             ExemplarID INTEGER PRIMARY KEY AUTOINCREMENT,
                             Bemerkung VARCHAR(255) NOT NULL
                         ); """

        table_titel = """ CREATE TABLE TITEL (
                          TitelID INTEGER PRIMARY KEY AUTOINCREMENT,
                          FachbereichsID int UNSIGNED NOT NULL,
                          Titel VARCHAR(255) NOT NULL,
                          ISBN INT(13) NULL DEFAULT NULL,
                          Autor VARCHAR(255) NOT NULL,
                          FOREIGN KEY (FachbereichsID) REFERENCES `FACHBEREICH`(`FachbereichsID`) ON DELETE CASCADE
                      ); """

        table_fachbereich = """ CREATE TABLE FACHBEREICH (
                                FachbereichsID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Fachbereichsname VARCHAR(255) NOT NULL
                            ); """

        cursor.execute(table_benutzer)
        cursor.execute(table_exemplar)
        cursor.execute(table_titel)
        cursor.execute(table_fachbereich)

        # Close the connection
        cursor.close()
        connection.close()
        

    # prited alles aus den tabellen
    def table_info(self):
        conn = sqlite3.connect('fms.db')
        c = conn.cursor()
        
        tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        for table_name in tables:
            table_name = table_name[0] # tables is a list of single item tuples
            table = pd.read_sql_query("SELECT * from {} LIMIT 0".format(table_name), conn)
            print(table_name)
            for col in table.columns:
                print('\t' + col)
            print()
        
        c.close()
        conn.close()


    def testsaetze(self):
        connection = sqlite3.connect('fms.db')
        cursor = connection.cursor()
        
        yadel = "INSERT INTO BENUTZER (Vorname, Nachname, Klasse) VALUES ('Yassin','Starzetz', 1011);"
        
        mrnoodle = "INSERT INTO BENUTZER (Vorname, Nachname, Klasse) VALUES ('Vincent','Starzetz', 1011);"
        
        cursor.execute(yadel)
        print(yadel)
        cursor.execute(mrnoodle)
        print(cursor.fetchall())
        
        cursor.close()
        connection.close()


    def get_benutzer(self):
        connection = sqlite3.connect('fms.db')
        cursor = connection.cursor()

        with connection:
            cursor.execute("SELECT * FROM BENUTZER;")
            print(cursor.fetchall())

        cursor.close()
        connection.close()


if __name__ == "__main__":
    
    Model().table_info()
    Model().testsaetze()
    Model().get_benutzer()
