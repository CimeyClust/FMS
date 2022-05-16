import os
import sqlite3 as sql
import pandas as pd
import datetime


class SQLiteModel(object):
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
                             DatumEntleihe DATE NULL DEFAULT NULL,
                             DatumRückgabe DATE NULL DEFAULT NULL,
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
                          Titelname VARCHAR(255) NOT NULL,
                          Autor VARCHAR(255) NOT NULL,
                          ISBN VARCHAR(13) NULL DEFAULT NULL,
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
            print(table_name + "\n", table, "\n")

    # Generell execute method for custom sql query
    def execute(self, query):
        self.cursor.execute(query)

    # Get Method for Tables
    def getTable(self, table_name: str, column: str):
        self.cursor.execute(f"SELECT {column} FROM {table_name};")
        return self.cursor.fetchall()

    # Insert methode for user
    def insertBenutzer(self, name: str, surname: str, school_class: int):
        self.cursor.execute(
            "INSERT INTO BENUTZER (Vorname, Nachname, Klasse) "
            "VALUES (?, ?, ?);", (name, surname, school_class)
        )

    def insertAusleihe(self, benutzer_id: int, exemplar_id: int, datum_entleihe: datetime, datum_rueckgabe: datetime):
        self.cursor.execute(
            "INSERT INTO AUSLEIHE (BenutzerID, ExemplarID, DatumEntleihe, DatumRückgabe) "
            "VALUES (?, ?, ?, ?);", (benutzer_id, exemplar_id, datum_entleihe, datum_rueckgabe)
        )

    def insertExemplar(self, titel_id: int, bemerkung: str):
        self.cursor.execute(
            "INSERT INTO EXEMPLAR (TitelID, Bemerkung) "
            "VALUES (?, ?);", (titel_id, bemerkung)
        )

    def insertTitel(self, fachbereichs_id: int, titelname: str, autor: str, isbn: str):
        self.cursor.execute(
            "INSERT INTO TITEL (FachbereichsID, Titelname, Autor, ISBN) "
            "VALUES (?, ?, ?, ?);", (fachbereichs_id, titelname, autor, isbn)
        )

    def insertFachbereich(self, fachbereichsname: str):
        self.cursor.execute("INSERT INTO FACHBEREICH (Fachbereichsname) "
                            "VALUES (?);", (fachbereichsname, ))

    # Get all IDs of the title entity
    def getTitleIDs(self):
        self.cursor.execute("SELECT TitelID FROM TITEL;")
        return self.cursor.fetchall()

    # Get the title of a Title entity by its id
    def getTitleTitle(self, titel_id: int):
        self.cursor.execute(f"SELECT Titel FROM TITEL WHERE TitelID = {titel_id};")
        return self.cursor.fetchone()

    # Get the isbn of a Title entity by its id
    def getTitleISBN(self, titel_id: int):
        self.cursor.execute(f"SELECT ISBN FROM TITEL WHERE TitelID = {titel_id};")
        return self.cursor.fetchone()

    # Get the author of a Title entity by its id
    def getTitleAuthor(self, titel_id: int):
        self.cursor.execute(f"SELECT Autor FROM TITEL WHERE TitelID = {titel_id};")
        return self.cursor.fetchone()

    # Get the subject id of a Title entity by its id
    def getTitleSubjectID(self, titel_id: int):
        self.cursor.execute(f"SELECT FachbereichsID FROM TITEL WHERE TitelID = {titel_id};")
        return self.cursor.fetchone()

    # Get all ids of the Fachwerk Entity
    def getSubjectIDs(self):
        self.cursor.execute("SELECT FachbereichsID FROM FACHBEREICH;")
        return self.cursor.fetchall()

    # Get the title of the subject by its FachwerkID
    def getSubjectName(self, titel_id: int):
        self.cursor.execute(f"SELECT Fachbereichsname FROM FACHBEREICH WHERE FachbereichsID = {titel_id};")
        return self.cursor.fetchone()

    def getStudentIDs(self):
        self.cursor.execute("SELECT BenutzerID FROM BENUTZER;")
        return self.cursor.fetchall()

<<<<<<< Updated upstream
    def getStudentSurName(self, benutzer_id: int):                 #-> str
        self.cursor.execute(f"SELECT Vorname FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getStudentLastName(self, benutzer_id: int):                # -> str
        self.cursor.execute(f"SELECT Nachname FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getStudentSchoolClass(self, benutzer_id: int):             #-> str
        self.cursor.execute(f"SELECT Klasse FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getBookIDs(self):                               #-> list(int)
        self.cursor.execute("SELECT ExemplarID FROM EXEMPLAR;")
        return self.cursor.fetchall()

    def isBookBorrowed(self, exemplar_id: int):                    #-> bool
        self.cursor.execute(f"SELECT  FROM EXEMPLAR WHERE ExemplarID = {exemplar_id};")
        return self.cursor.fetchone()
=======
    def getStudentSurName(self, benutzer_id: int):  # -> str
        self.cursor.execute(f"SELECT Vorname FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getStudentLastName(self, benutzer_id: int):  # -> str
        self.cursor.execute(f"SELECT Nachname FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getStudentSchoolClass(self, benutzer_id: int):  # -> str
        self.cursor.execute(f"SELECT Klasse FROM BENUTZER WHERE BenutzerID = {benutzer_id};")
        return self.cursor.fetchone()

    def getBookIDs(self):  # -> list(int)
        self.cursor.execute("SELECT ExemplarID FROM EXEMPLAR;")
        return self.cursor.fetchall()

    def isBookBorrowed(self, exemplar_id: int):  # -> bool
        self.cursor.execute(f"SELECT ExemplarID FROM AUSLEIHE WHERE ExemplarID = {exemplar_id};")
        if self.cursor.fetchone() is None:
            return False

        return True
>>>>>>> Stashed changes

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
    SQLiteModel().dumpDatabase()
    with SQLiteModel() as db:
        db.insertBenutzer("Yassin", "Starzetz", 1011)
        db.insertBenutzer("Luis", "Hamann", 1011)
        db.insertBenutzer("Leon", "Martin", 1011)
        db.insertFachbereich("Mathe")
        db.insertFachbereich("Englisch")
        db.insertTitel(1, "Math - the Book", "Dr. Bum", "1154848942134")
        db.insertTitel(1, "1 + 1 die Basics", "Smith Johnson", "1157496342456")
        db.insertTitel(2, "learn english", "Erwin Arlert", "1685645422381")
        db.insertExemplar(1, "sieht gut aus")
        db.insertExemplar(2, "bisl zerkratzt")
        db.insertExemplar(2, "Flasche ausgeschüttet")
        db.insertExemplar(3, "wurde aus Versehen verbrannt")
        db.insertExemplar(3, "wurde reingemalt")
        db.insertAusleihe(1, 1, datetime.date.today(), datetime.date.today())
        db.insertAusleihe(2, 3, datetime.date.today(), datetime.date.today())
        db.insertAusleihe(3, 4, datetime.date.today(), datetime.date.today())
        db.tableInfo()
        print(db.getTable("BENUTZER", "*"))
        print(db.getTable("BENUTZER", "Vorname, Nachname"))
        db.dumpTable(['BENUTZER', 'AUSLEIHE', 'EXEMPLAR', 'TITEL', 'FACHWERK'])
