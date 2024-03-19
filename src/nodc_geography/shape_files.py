import functools
import pathlib
import sys

import geopandas as gpd
import yaml
from shapely.geometry import Point

import logging

logger = logging.getLogger(__name__)


if getattr(sys, 'frozen', False):
    THIS_DIR = pathlib.Path(sys.executable).parent
else:
    THIS_DIR = pathlib.Path(__file__).parent

SHAPE_FILES_DIR = THIS_DIR / 'SHAPE_FILES'


class ShapeFilesConfig:

    def __init__(self, path: str | pathlib.Path) -> None:
        self._path = pathlib.Path(path)
        self._config = dict()
        self._variable_to_path_mapping = dict()
        self._file_mapping = dict()
        self._load_file()
        self._save_mapping()

    def _load_file(self) -> None:
        with open(self._path) as fid:
            self._config = yaml.safe_load(fid)

    def _save_mapping(self) -> None:
        for item in self._config:
            if not item.get('active'):
                continue
            file_stem = item['name']
            self._file_mapping[file_stem] = item
            for variable in item['mapping']:
                if self._variable_to_path_mapping.get(variable):
                    logger.warning(f'Variable already added from other file: {variable} (duplicate in '
                                            f'{file_stem})')
                    continue
                file_path = SHAPE_FILES_DIR / f'{file_stem}.shp'
                if not file_path.exists():
                    logger.warning(f'Shape file does not exist: {file_path}')
                    continue
                self._variable_to_path_mapping[variable] = file_path

    def get_translations_for_file(self, file_path: pathlib.Path) -> dict:
        file_stem = file_path.stem
        if not self._file_mapping.get(file_stem):
            logger.error(f'No configuration found for shapefile: {file_stem}')
            return {}
        print(f'{self._file_mapping[file_stem]=}')
        if not self._file_mapping[file_stem].get('active'):
            logger.error(f'Configuration for shapefile {file_stem} is not active!')
            return {}
        return self._file_mapping[file_stem]['mapping']

    def get_file_path_for_variable(self, variable: str) -> pathlib.Path:
        return self._variable_to_path_mapping.get(variable)


class ShapeFile:

    def __init__(self, path: str | pathlib.Path, epsg: str = '3006', **kwargs):
        self._path = pathlib.Path(path)
        self._epsg = 'EPSG:' + epsg.split(':')[-1]
        self._translation = dict()
        self._load_file()

    @property
    def _epsg_nr(self):
        return self._epsg.split(':')[1]

    def _load_file(self):
        self._gdf = gpd.read_file(self._path)
        self._gdf.crs = self._epsg

    def set_translation(self, translation: dict):
        self._translation = translation

    @functools.cache
    def get(self, x_pos: float, y_pos: float, variable: str) -> str | None:
        """Returns the value for the given variable at given position.
        variable kan be location_county, location_water_district etc.
        the variable is mapped by the column_translation to match the files internal variable"""
        boolean = self._gdf.contains(Point(x_pos, y_pos))
        translated_variable = self._translation.get(variable)
        if not translated_variable:
            logger.warning(f'No translation found for variable: {variable}')
            return
        if translated_variable not in self._gdf.columns:
            logger.warning(f'Translated variable {translated_variable} not in file {self._path}')
            return
        filtered = self._gdf[boolean][translated_variable]
        if len(filtered) != 1:
            logger.warning(f'{len(filtered)} posts found for pos: {x_pos}-{y_pos} and variable:'
                                          f' {translated_variable}')
            return
        return filtered.values[0]


