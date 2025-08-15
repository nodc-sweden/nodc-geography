import sqlite3

from nodc_geography.paths import CONFIG_DIRECTORY

DB_PATH = CONFIG_DIRECTORY / "lookup_database.db"


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x_pos REAL,
            y_pos REAL,
            variable TEXT,
            name TEXT, 
            UNIQUE(x_pos, y_pos, variable)
        );
        """

        cursor.execute(create_table_query)

        connection.commit()
        print("Location database created!")


def add(x_pos: float, y_pos: float, variable: str, name: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Locations (x_pos, y_pos, variable, name) 
        VALUES (?, ?, ?, ?);
        """
        data = (x_pos, y_pos, variable, name)

        cursor.execute(insert_query, data)

        connection.commit()


def get(x_pos: float, y_pos: float, variable: str) -> str:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
           SELECT * FROM Locations 
           WHERE x_pos = ? 
           AND y_pos = ? 
           AND variable = ?
           ;
           """
        data = (x_pos, y_pos, variable)

        cursor.execute(query, data)
        result = cursor.fetchone()

        connection.commit()
        if result:
            return result[-1]


create_database()
