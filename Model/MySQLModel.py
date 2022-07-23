###########################################################################
#
# MySQLModel.py
# Program made by Leon and Yassin for the FMS project.
#
###########################################################################

# import sqlite3 as sql
import asyncio
import tkinter.filedialog

import pandas as pd
import datetime
import os
import qrcode
import mysql.connector as sql


###########################################################################
#
#    The Database class of the FMS.
#
#    [what this class does]
#
###########################################################################

class MySQLModel(object):

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

    def __init__(self, host: str, user: str, password: str, databaseName: str):
        try:
            mysql_config = {
                'user': user,
                'password': password,
                'host': host.split(":")[0],
                'database': databaseName,
                'port': host.split(":")[1],
                'ssl_disabled': True
            }
        except IndexError:
            mysql_config = {
                'user': user,
                'password': password,
                'host': host.split(":")[0],
                'database': databaseName,
                'port': 3306,
                'ssl_disabled': True
            }
        self.connection = sql.connect(**mysql_config)
        self.cursor = self.connection.cursor()
        self.resolve(self.createTable)

    def isConnected(self):
        return self.connection.is_connected()

    #######################################################################
    #
    #  Function to create tables.
    #
    #  This function builds the necessary tables for the FMS in order to
    #  work properly.
    #
    #######################################################################

    async def createTable(self):
        # Creating SQL queries for the table generation
        table_schueler = """ CREATE TABLE IF NOT EXISTS `SCHUELER` ( 
                                `SchuelerID` INT NOT NULL AUTO_INCREMENT , 
                                `Vorname` VARCHAR(255) NOT NULL , 
                                `Nachname` VARCHAR(255) NOT NULL , 
                                `Klasse` VARCHAR(255) NOT NULL , 
                                PRIMARY KEY (`SchuelerID`)
                             ) 
                             ENGINE = InnoDB; """

        table_ausleihe = """ CREATE TABLE IF NOT EXISTS `AUSLEIHE` ( 
                                `VorgangsID` INT NOT NULL AUTO_INCREMENT , 
                                `SchuelerID` INT UNSIGNED NOT NULL , 
                                `ExemplarID` INT UNSIGNED NOT NULL , 
                                `DatumEntleihe` DATE NULL DEFAULT NULL , 
                                PRIMARY KEY (`VorgangsID`)
                             ) 
                             ENGINE = InnoDB; """

        ausleihe_foreign_students = """ ALTER TABLE `AUSLEIHE` 
                                ADD CONSTRAINT `AUSLEIHE_SchuelerID_SCHUELER_SchuelerID` 
                                FOREIGN KEY (`SchuelerID`) REFERENCES `SCHUELER`(`SchuelerID`); """

        ausleihe_foreign_books = """ ALTER TABLE `AUSLEIHE` 
                                ADD CONSTRAINT `AUSLEIHE_ExemplarID_EXEMPLAR_ExemplarID` 
                                FOREIGN KEY (`ExemplarID`) REFERENCES `EXEMPLAR`(`ExemplarID`); """

        table_exemplar = """ CREATE TABLE IF NOT EXISTS `EXEMPLAR` ( 
                                `ExemplarID` INT NOT NULL AUTO_INCREMENT , 
                                `TitelID` INT UNSIGNED NOT NULL , 
                                `Bemerkung` VARCHAR(255) NOT NULL , 
                                PRIMARY KEY (`ExemplarID`)
                             ) 
                             ENGINE = InnoDB;"""

        ausleihe_foreign_book = """ ALTER TABLE `EXEMPLAR` 
                                ADD CONSTRAINT `EXEMPLAR_TitelID_TITEL_TitelID` 
                                FOREIGN KEY (`TitelID`) REFERENCES `TITEL`(`TitelID`); """

        table_titel = """ CREATE TABLE IF NOT EXISTS `TITEL` ( 
                            `TitelID` INT NOT NULL AUTO_INCREMENT , 
                            `FachbereichsID` INT UNSIGNED NOT NULL , 
                            `Titelname` VARCHAR(255) NOT NULL , `Autor` 
                            VARCHAR(255) NOT NULL , `ISBN` VARCHAR(13) NOT NULL , 
                            PRIMARY KEY (`TitelID`)
                          ) 
                          ENGINE = InnoDB; """

        ausleihe_foreign_title = """ ALTER TABLE `TITEL` ADD CONSTRAINT `TITLE_FACHBEREICH` 
                                     FOREIGN KEY (`FachbereichsID`) REFERENCES `FACHBEREICH`(`FachbereichsID`) 
                                     ON DELETE CASCADE ON UPDATE CASCADE; """

        table_fachbereich = """ CREATE TABLE IF NOT EXISTS `FACHBEREICH` ( 
                                `FachbereichsID` INT NOT NULL AUTO_INCREMENT , 
                                `Fachbereichsname` VARCHAR(255) NOT NULL , 
                                PRIMARY KEY (`FachbereichsID`)) 
                                ENGINE = InnoDB; 
                            """

        # Execution of the SQL queries
        self.cursor.execute(table_fachbereich)

        self.cursor.execute(table_titel)
        # self.cursor.execute(ausleihe_foreign_title)

        self.cursor.execute(table_schueler)

        self.cursor.execute(table_exemplar)
        # self.cursor.execute(ausleihe_foreign_book)

        self.cursor.execute(table_ausleihe)
        # self.cursor.execute(ausleihe_foreign_students)
        # self.cursor.execute(ausleihe_foreign_books)

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

    async def insertSchueler(self, vorname: str, nachname: str, klasse: str):
        self.cursor.execute(
            "INSERT INTO SCHUELER (Vorname, Nachname, Klasse) "
            "VALUES (%s, %s, %s);", (vorname, nachname, klasse)
        )
        self.cursor.execute(
            f"SELECT SchuelerID FROM SCHUELER WHERE Vorname = '{vorname}' AND Nachname = '{nachname}' AND Klasse = '{klasse}';")
        return self.cursor.fetchone()

    async def insertAusleihe(self, student_id: int, exemplar_id: int, datum_entleihe: datetime):
        self.cursor.execute(
            "INSERT INTO AUSLEIHE (SchuelerID, ExemplarID, DatumEntleihe) "
            "VALUES (%s, %s, %s);", (student_id, exemplar_id, datum_entleihe)
        )
        self.cursor.execute(
            f"SELECT VorgangsID FROM AUSLEIHE WHERE SchuelerID = {student_id} AND ExemplarID = {exemplar_id} AND DatumEntleihe = {datum_entleihe} ")
        return self.cursor.fetchone()

    def getAusleiheID(self, student_id: int, exemplar_id: int):
        self.cursor.execute(
            f"SELECT VorgangsID FROM AUSLEIHE WHERE SchuelerID = {student_id} AND ExemplarID = {exemplar_id} ")
        return self.cursor.fetchone()

    async def insertExemplar(self, titel_id: int, bemerkung: str):
        self.cursor.execute(
            "INSERT INTO EXEMPLAR (TitelID, Bemerkung) VALUES (%s, %s);", (titel_id, bemerkung)
        )
        self.cursor.execute(
            f"SELECT ExemplarID FROM EXEMPLAR WHERE TitelID = {titel_id} AND Bemerkung = '{bemerkung}'")
        return self.cursor.fetchall()

    async def insertTitel(self, fachbereichs_id: int, titelname: str, autor: str, isbn: str):
        self.cursor.execute(
            "INSERT INTO TITEL (FachbereichsID, Titelname, Autor, ISBN) "
            "VALUES (%s, %s, %s, %s);", (fachbereichs_id, titelname, autor, isbn)
        )
        self.cursor.execute(
            f"SELECT TitelID FROM TITEL WHERE FachbereichsID = {fachbereichs_id} AND Titelname = '{titelname}' AND Autor = '{autor}' AND ISBN = {isbn}"
        )
        return self.cursor.fetchone()

    async def insertFachbereich(self, fachbereichsname: str):
        self.cursor.execute(
            "INSERT INTO FACHBEREICH (Fachbereichsname) "
            "VALUES (%s);", (fachbereichsname,)
        )
        self.cursor.execute(
            f"SELECT FachbereichsID FROM FACHBEREICH WHERE Fachbereichsname = '{fachbereichsname}'"
        )
        return self.cursor.fetchone()

    # UPDATE

    async def updateTitle(self, titleID: int, titleName: str, isbn: str, author: str, subjectID: int):
        statement = f"UPDATE TITEL SET Titelname = '{titleName}', Autor = '{author}', ISBN = '{isbn}', FachbereichsID = {subjectID} WHERE TitelID = {titleID};"
        self.cursor.execute(statement)

    # DELETE

    async def deleteRow(self, table_name: str, tableIDColumn: str, row_id: int):
        statement = f"DELETE FROM {table_name} WHERE {tableIDColumn} = {row_id};"
        self.cursor.execute(statement)

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

    async def executeQuery(self, query):
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
        path = tkinter.filedialog.askdirectory(initialdir=os.path.expanduser("~"))
        try: img.save(path + "\\Books\\Book" + str(id) + ".png")
        except OSError:
            os.mkdir(path + "\\Books")
            img.save(path + "\\Books\\Book" + str(id) + ".png")

    def resolve(self, method, *args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(method(*args))
        return result


if __name__ == "__main__":
    os.remove("fms.db")
    with MySQLModel() as db:
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
