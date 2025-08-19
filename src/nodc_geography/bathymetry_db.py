import sqlite3

from nodc_geography.paths import BATHYMETRY_DIRECTORY

DB_PATH = BATHYMETRY_DIRECTORY / "bathymetry_database.db"
print(f"Bathymetry database ")


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Bathymetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL,
            depth REAL,
            file_name TEXT,
            UNIQUE(lat, lon, file_name)
        );
        """

        cursor.execute(create_table_query)

        connection.commit()


def add(lat: float, lon: float, depth: float, file_name: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Bathymetry (lat, lon, depth, file_name) 
        VALUES (?, ?, ?, ?);
        """
        data = (lat, lon, depth, file_name)

        cursor.execute(insert_query, data)

        connection.commit()


def get(lat: float, lon: float) -> float:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        query = """
           SELECT * FROM Bathymetry 
           WHERE lat = ? 
           AND lon = ? 
           ;
           """
        data = (lat, lon)

        cursor.execute(query, data)
        result = cursor.fetchone()

        connection.commit()
        if result:
            return result[-2]


create_database()
