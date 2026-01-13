import sqlite3
from typing import Any

from nodc_geography.paths import CONFIG_DIRECTORY

DB_PATH = CONFIG_DIRECTORY / "location_database.db"
print(f"Location database at {DB_PATH}")

COLUMNS = [
    "id",
    "x_pos",
    "y_pos",
    "variable",
    "name",
]


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x_pos TEXT,
            y_pos TEXT,
            variable TEXT,
            name TEXT, 
            UNIQUE(x_pos, y_pos, variable)
        );
        """

        cursor.execute(create_table_query)

        connection.commit()


def add(x_pos: float, y_pos: float, variable: str, name: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Locations (x_pos, y_pos, variable, name) 
        VALUES (?, ?, ?, ?);
        """
        name = name or ""
        data = (x_pos, y_pos, variable, name)

        cursor.execute(insert_query, data)

        connection.commit()


def add_multiple(x_pos: list[float],
                 y_pos: list[float],
                 variable: list[str],
                 name: list[str]):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT OR IGNORE INTO Locations (x_pos, y_pos, variable, name) 
        VALUES (?, ?, ?, ?);
        """
        data = []
        for x, y, va, na in zip(x_pos, y_pos, variable, name):
            data.append((x, y, va, str(na or "")))

        cursor.executemany(insert_query, data)

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


def get_all_for_position(x_pos: float, y_pos: float) -> dict[str, str]:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
           SELECT * FROM Locations 
           WHERE x_pos = ? 
           AND y_pos = ? 
           ;
           """
        data = (x_pos, y_pos)

        cursor.execute(query, data)
        result = cursor.fetchall()

        connection.commit()
        info = dict()
        for item in result:
            item_dict = dict(zip(COLUMNS, item))
            info[item_dict["variable"]] = item_dict["name"]
        return info
        # if result:
        #     return result[-1]


create_database()
