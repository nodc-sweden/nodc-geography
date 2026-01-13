import sqlite3

import geopy.distance

from nodc_geography.paths import BATHYMETRY_DIRECTORY

DB_PATH = BATHYMETRY_DIRECTORY / "bathymetry_database.db"
print(f"Bathymetry database ")

COLUMNS = [
    "lat",
    "lon",
    "z",
    "match_lat",
    "match_lon",
    "dist_m",
    "source_file_name"
]


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Bathymetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL,
            z REAL,
            match_lat REAL,
            match_lon REAL,
            dist_m REAL,
            source_file_name TEXT,
            UNIQUE(lat, lon, source_file_name)
        );
        """

        cursor.execute(create_table_query)

        connection.commit()


def add(lat: float, lon: float, z: float, source_file_name: str,
        match_lat: float, match_lon: float, **kwargs):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Bathymetry (lat, lon, z, match_lat, match_lon, dist_m, source_file_name) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """

        cord1 = (lat, lon)
        cord2 = (match_lat, match_lon)

        dist_m = geopy.distance.geodesic(cord1, cord2).m

        data = (lat, lon, z, match_lat, match_lon, dist_m, source_file_name)

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
            return dict(zip(COLUMNS, result[1:]))
            # return result[3]


create_database()
