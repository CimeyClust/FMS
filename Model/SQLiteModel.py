###########################################################################
#
# Model.py
# Program made by Luis and Yassin for the FMS project.
#
###########################################################################

import sqlite3 as sql
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
        self.connection = sql.connect('fms.db')
        self.cursor = self.connection.cursor()
        self.createTable()

        # Local AppData Directory --> self.connection = sql.connect(f'{os.getenv("LOCALAPPDATA")}\\fms.db')

    #######################################################################
    #
    #  Function to create tables.
    #
    #  This function builds the necessary tables for the FMS in order to
    #  work properly.
    #
    #######################################################################

    def createTable(self):
        # Creating SQL queries for the table generation
        table_schueler = """ CREATE TABLE IF NOT EXISTS SCHUELER (
                             SchuelerID INTEGER PRIMARY KEY,
                             Vorname VARCHAR(255) NOT NULL,
                             Nachname VARCHAR(255) NOT NULL,
                             Klasse VARCHAR(255) NULL DEFAULT NULL
                         ); """

        table_ausleihe = """ CREATE TABLE IF NOT EXISTS AUSLEIHE (
                             VorgangsID INTEGER PRIMARY KEY,
                             SchuelerID INTEGER UNSIGNED NOT NULL,
                             ExemplarID INTEGER UNSIGNED NOT NULL,
                             DatumEntleihe DATE NULL DEFAULT NULL,
                             FOREIGN KEY (SchuelerID) REFERENCES `SCHUELER`(`SchuelerID`) ON DELETE CASCADE,
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
        self.cursor.execute(table_schueler)
        self.cursor.execute(table_ausleihe)
        self.cursor.execute(table_exemplar)
        self.cursor.execute(table_titel)
        self.cursor.execute(table_fachbereich)

    #######################################################################
    #
    #  Function to delete one or multiple tables.
    #
    #  @param tables: A list containing strings with the name of a table.
    #
    #######################################################################

    def dumpTable(self, tables: list):
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")

    #######################################################################
    #
    #  Function to return information about all tables in the database.
    #
    #  This function is only meant for debugging. It allows to view
    #  all information about the database inside the console and is not
    #  meant for any practise other than that.
    #
    #######################################################################

    def tableInfo(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            table = pd.read_sql_query(f"SELECT * from {table_name}", self.connection)
            print(table_name + "\n", table, "\n")

    #######################################################################
    #
    #  Function to query data from the database.
    #
    #  This is the main function to get data from the database.
    #  It can either get all data or only the data from one or more columns
    #  of a table.
    #
    #  @param table_name: The name of the database's table to query from.
    #
    #  @param column: A string of columns, comma-separated.
    #
    #######################################################################

    def getTable(self, table_name: str, column: str):
        self.cursor.execute(f"SELECT {column} FROM {table_name};")
        return self.cursor.fetchall()

    #######################################################################
    #
    #  Functions to query specific data from the database.
    #
    #######################################################################

    # Get all IDs of the title entity
    def getTitleIDs(self):
        self.cursor.execute("SELECT TitelID FROM TITEL;")
        return self.cursor.fetchall()

    # Get the title of a Title entity by its id
    def getTitleTitle(self, titel_id: int):
        self.cursor.execute(f"SELECT Titelname FROM TITEL WHERE TitelID = {titel_id};")
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
    def getSubjectName(self, subjectID: int):
        self.cursor.execute(f"SELECT Fachbereichsname FROM FACHBEREICH WHERE FachbereichsID = {subjectID};")
        return self.cursor.fetchone()

    def getStudentIDs(self):
        self.cursor.execute("SELECT SchuelerID FROM SCHUELER;")
        return self.cursor.fetchall()

    def getStudentID(self, vorname: str, nachname: str, klasse: str):
        self.cursor.execute(
            f"SELECT SchuelerID FROM SCHUELER WHERE Vorname = {vorname} AND Nachname = {nachname} AND Klasse = '{klasse}';")
        return self.cursor.fetchone()

    def getStudentSurName(self, student_id: int):  # -> str
        self.cursor.execute(f"SELECT Vorname FROM SCHUELER WHERE SchuelerID = {student_id};")
        return self.cursor.fetchone()

    def getStudentLastName(self, student_id: int):  # -> str
        self.cursor.execute(f"SELECT Nachname FROM SCHUELER WHERE SchuelerID = {student_id};")
        return self.cursor.fetchone()

    def getStudentSchoolClass(self, student_id: int):  # -> str
        self.cursor.execute(f"SELECT Klasse FROM SCHUELER WHERE SchuelerID = {student_id};")
        return self.cursor.fetchone()

    def getBookIDs(self):  # -> list(int)
        self.cursor.execute("SELECT ExemplarID FROM EXEMPLAR;")
        return self.cursor.fetchall()

    def getBookTitleID(self, bookID):
        self.cursor.execute(f"SELECT TitelID FROM EXEMPLAR WHERE ExemplarID = {bookID};")
        return self.cursor.fetchone()

    def getBookStudentID(self, bookID):
        self.cursor.execute(f"SELECT SchuelerID FROM AUSLEIHE WHERE ExemplarID = {bookID};")
        return self.cursor.fetchone()

    def isBookBorrowed(self, exemplar_id: int):  # -> bool
        self.cursor.execute(f"SELECT ExemplarID FROM AUSLEIHE WHERE ExemplarID = {exemplar_id};")
        if self.cursor.fetchone() is None:
            return False

        return True

    #######################################################################
    #
    #  Functions to insert new data into the database.
    #
    #  @method insertSchueler:
    #  takes 3 parameters [Vorname, Nachname, Klasse]
    #
    #  @method insertAusleihe:
    #  takes 4 parameters [SchuelerID, ExemplarID, DatumEntleihe]
    #
    #  @method insertExemplar:
    #  takes 2 parameters [TitelID, Bemerkung]
    #
    #  @method insertTitel:
    #  takes 4 parameters [FachbereichsID, Titelname, Autor, ISBN]
    #
    #  @method insertFachbereich:
    #  takes 1 parameter [Fachbereichsname]
    #
    #######################################################################

    def insertSchueler(self, vorname: str, nachname: str, klasse: str):
        self.cursor.execute(
            "INSERT INTO SCHUELER (Vorname, Nachname, Klasse) "
            "VALUES (?, ?, ?);", (vorname, nachname, klasse)
        )
        self.cursor.execute(
            f"SELECT SchuelerID FROM SCHueLER WHERE Vorname = '{vorname}' AND Nachname = '{nachname}' AND Klasse = '{klasse}';")
        return self.cursor.fetchone()

    def insertAusleihe(self, student_id: int, exemplar_id: int, datum_entleihe: datetime):
        self.cursor.execute(
            "INSERT INTO AUSLEIHE (SchuelerID, ExemplarID, DatumEntleihe) "
            "VALUES (?, ?, ?);", (student_id, exemplar_id, datum_entleihe)
        )
        self.cursor.execute(
            f"SELECT VorgangsID FROM AUSLEIHE WHERE SchuelerID = {student_id} AND ExemplarID = {exemplar_id} AND DatumEntleihe = {datum_entleihe} ")
        return self.cursor.fetchone()

    def getAusleiheID(self, student_id: int, exemplar_id: int):
        self.cursor.execute(
            f"SELECT VorgangsID FROM AUSLEIHE WHERE SchuelerID = {student_id} AND ExemplarID = {exemplar_id} ")
        return self.cursor.fetchone()

    def insertExemplar(self, titel_id: int, bemerkung: str):
        self.cursor.execute(
            "INSERT INTO EXEMPLAR (TitelID, Bemerkung) "
            "VALUES (?, ?);", (titel_id, bemerkung)
        )
        self.cursor.execute(
            f"SELECT ExemplarID FROM EXEMPLAR WHERE TitelID = {titel_id} AND Bemerkung = '{bemerkung}'")
        return self.cursor.fetchone()

    def insertTitel(self, fachbereichs_id: int, titelname: str, autor: str, isbn: str):
        self.cursor.execute(
            "INSERT INTO TITEL (FachbereichsID, Titelname, Autor, ISBN) "
            "VALUES (?, ?, ?, ?);", (fachbereichs_id, titelname, autor, isbn)
        )
        self.cursor.execute(
            f"SELECT TitelID FROM TITEL WHERE FachbereichsID = {fachbereichs_id} AND Titelname = '{titelname}' AND Autor = '{autor}' AND ISBN = {isbn}"
        )
        return self.cursor.fetchone()

    def insertFachbereich(self, fachbereichsname: str):
        self.cursor.execute(
            "INSERT INTO FACHBEREICH (Fachbereichsname) "
            "VALUES (?);", (fachbereichsname,)
        )
        self.cursor.execute(
            f"SELECT FachbereichsID FROM FACHBEREICH WHERE Fachbereichsname = '{fachbereichsname}'"
        )
        return self.cursor.fetchone()

    # UPDATE

    def updateTitle(self, titleID: int, titleName: str, isbn: str, author: str, subjectID: int):
        statement = f"UPDATE TITEL SET Titelname = '{titleName}', Autor = '{author}', ISBN = '{isbn}', FachbereichsID = {subjectID} WHERE TitelID = {titleID};"
        self.cursor.execute(statement)

    # DELETE

    def deleteRow(self, table_name: str, tableIDColumn: str, row_id: int):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {tableIDColumn} = {row_id};")

    #######################################################################
    #
    #  Function to query any other SQL statement.
    #
    #  This function is there in case it's wanted to execute any other sql
    #  statement other than the given ones.
    #
    #  @param query: A valid SQL statement in string format.
    #
    #######################################################################

    def executeQuery(self, query):
        self.cursor.execute(query)

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

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.getcwd() + "\\Book" + str(id) + ".png")


if __name__ == "__main__":
    os.remove("fms.db")
    with SQLiteModel() as db:
        db.insertSchueler("Yassin", "Starzetz", "1011")
        db.insertSchueler("Luis", "Hamann", "1011")
        db.insertSchueler("Leon", "Martin", "1011")
        db.insertFachbereich("Mathe")
        db.insertFachbereich("Englisch")
        db.insertTitel(1, "Math - the Book", "Dr. Bum", "1154848942134")
        db.insertTitel(1, "1 + 1 die Basics", "Smith Johnson", "1157496342456")
        db.insertTitel(2, "learn english", "Erwin Arlert", "1685645422381")
        db.insertExemplar(1, "sieht gut aus")
        db.insertExemplar(2, "bisschen zerkratzt")
        db.insertExemplar(2, "Flasche ausgeschüttet")
        db.insertExemplar(3, "wurde aus Versehen verbrannt")
        db.insertExemplar(3, "wurde reingemalt")
        db.insertAusleihe(1, 1, datetime.date.today())
        db.insertAusleihe(2, 3, datetime.date.today())
        db.insertAusleihe(3, 4, datetime.date.today())

        db.tableInfo()

        print(db.getTable("SCHUELER", "*"))
        print(db.getTable("SCHUELER", "Vorname, Nachname"))
        db.dumpTable(['SCHUELER', 'AUSLEIHE', 'EXEMPLAR', 'TITEL', 'FACHWERK'])
