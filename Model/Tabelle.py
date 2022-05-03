import sqlite3


# Define connection and cursor
connection = sqlite3.connect('fms.db')
cursor = connection.cursor()

# Creating table
table_benutzer = """ CREATE TABLE BENUTZER (
                     BenutzerID INTEGER PRIMARY KEY AUTOINCREMENT,
                     Vorname VARCHAR(255) NOT NULL,
                     Nachname VARCHAR(255) NOT NULL,
                     Klasse INT(4) NULL DEFAULT NULL
                 ); """

table_entleiht = """ CREATE TABLE ENTLEIHT (
                     VorgangsID INTEGER PRIMARY KEY AUTOINCREMENT,
                     BenutzerID INTEGER UNSIGNED NOT NULL,
                     ExemplarID INTEGER UNSIGNED NOT NULL,
                     DatumEntleihe TIMESTAMP NOT NULL,
                     DatumRückgabe TIMESTAMP NOT NULL,
                     FOREIGN KEY (BenutzerID) REFERENCES `BENUTZER`(`BenutzerID`) ON DELETE CASCADE,
                     FOREIGN KEY (ExemplarID) REFERENCES `EXEMPLAR`(`ExemplarID`) ON DELETE CASCADE
                 ); """

table_exemplar = """ CREATE TABLE EXEMPLAR (
                     ExemplarID INTEGER PRIMARY KEY AUTOINCREMENT,
                     TitelID INTEGER UNSIGNED NOT NULL,
                     Bemerkung VARCHAR(255) NOT NULL,
                     FOREIGN KEY (TitelID) REFERENCES `TITEL`(`TitelID`) ON DELETE CASCADE
                 ); """

table_titel = """ CREATE TABLE TITEL (
                  TitelID INTEGER PRIMARY KEY AUTOINCREMENT,
                  FachbereichsID INTEGER UNSIGNED NOT NULL,
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
cursor.execute(table_entleiht)
cursor.execute(table_exemplar)
cursor.execute(table_titel)
cursor.execute(table_fachbereich)

# Close the connection
cursor.close()
connection.close()

