    def to_csv(self):
        connection = sqlite3.connect('fms.db')
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            table = pd.read_sql_query(f"SELECT * from {table_name}", connection)
            table.to_csv(table_name + '.csv', index_label='index')
            print("\n" + table_name)
            print(table)

        cursor.close()
        connection.close()

    print("\n" + os.getenv('LOCALAPPDATA'))