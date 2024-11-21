import functools
import logging
import os
import pathlib
import ssl
import requests

from nodc_geography import shape_files

logger = logging.getLogger(__name__)

CONFIG_SUBDIRECTORY = 'nodc_geography'
CONFIG_FILE_NAMES = [
    'shape_file_config.yaml',
    'SHAPE_FILES',
]

SHAPE_FILES = [
    '1 Shapefile-översikt.txt',
    'ak_riks.cpg',
    'ak_riks.dbf',
    'ak_riks.prj',
    'ak_riks.qix',
    'ak_riks.shp',
    'ak_riks.shx',
    'an_riks.cpg',
    'an_riks.dbf',
    'an_riks.prj',
    'an_riks.qix',
    'an_riks.shp',
    'an_riks.shx',
    'havdirtyper_2012_delatKattegatt.dbf',
    'havdirtyper_2012_delatKattegatt.prj',
    'havdirtyper_2012_delatKattegatt.qix',
    'havdirtyper_2012_delatKattegatt.sbn',
    'havdirtyper_2012_delatKattegatt.sbx',
    'havdirtyper_2012_delatKattegatt.shp',
    'havdirtyper_2012_delatKattegatt.shp.xml',
    'havdirtyper_2012_delatKattegatt.shx',
    'Havsomr_SVAR_2016_3b_CP1252.dbf',
    'Havsomr_SVAR_2016_3b_CP1252.qix',
    'Havsomr_SVAR_2016_3b_CP1252.shp',
    'Havsomr_SVAR_2016_3b_CP1252.shx',
    'Havsomr_SVAR_2016_3c_CP1252.dbf',
    'Havsomr_SVAR_2016_3c_CP1252.qix',
    'Havsomr_SVAR_2016_3c_CP1252.shp',
    'Havsomr_SVAR_2016_3c_CP1252.shx',
    'havsomr_y_2012_2.dbf',
    'havsomr_y_2012_2.prj',
    'havsomr_y_2012_2.qix',
    'havsomr_y_2012_2.sbn',
    'havsomr_y_2012_2.sbx',
    'havsomr_y_2012_2.shp',
    'havsomr_y_2012_2.shp.xml',
    'havsomr_y_2012_2.shx',
    'KOMMUNER_LAN.dbf',
    'KOMMUNER_LAN.prj',
    'KOMMUNER_LAN.qix',
    'KOMMUNER_LAN.sbn',
    'KOMMUNER_LAN.sbx',
    'KOMMUNER_LAN.shp',
    'KOMMUNER_LAN.shp.xml',
    'KOMMUNER_LAN.shx',
    'KONVENTION.dbf',
    'KONVENTION.prj',
    'KONVENTION.qix',
    'KONVENTION.sbn',
    'KONVENTION.sbx',
    'KONVENTION.shp',
    'KONVENTION.shx',
    'MSFD_areas.dbf',
    'MSFD_areas.prj',
    'MSFD_areas.qix',
    'MSFD_areas.sbn',
    'MSFD_areas.sbx',
    'MSFD_areas.shp',
    'MSFD_areas.shp.xml',
    'MSFD_areas.shx',
    'MSFD_areas_TM.dbf',
    'MSFD_areas_TM.prj',
    'MSFD_areas_TM.qpj',
    'MSFD_areas_TM.shp',
    'MSFD_areas_TM.shx',
]


CONFIG_DIRECTORY = None
if os.getenv('NODC_CONFIG'):
    CONFIG_DIRECTORY = pathlib.Path(os.getenv('NODC_CONFIG')) / CONFIG_SUBDIRECTORY
TEMP_CONFIG_DIRECTORY = pathlib.Path.home() / 'temp_nodc_config' / CONFIG_SUBDIRECTORY


# CONFIG_URL = r'https://raw.githubusercontent.com/nodc-sweden/nodc_config/refs/heads/main/' + f'{CONFIG_SUBDIRECTORY}/'
CONFIG_URL = r'https://github.com/nodc-sweden/nodc_config/raw/refs/heads/main/' + f'{CONFIG_SUBDIRECTORY}/'


def get_config_path(name: str) -> pathlib.Path:
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    if CONFIG_DIRECTORY:
        path = CONFIG_DIRECTORY / name
        if path.exists():
            return path
    temp_path = TEMP_CONFIG_DIRECTORY / name
    if temp_path.exists():
        return temp_path
    update_config_file(temp_path)
    if temp_path.exists():
        return temp_path
    raise FileNotFoundError(f'Could not find config file {name}')


def update_config_file(path: pathlib.Path) -> None:
    if path.name == 'SHAPE_FILES':
        # update_shape_files()
        return
    path.parent.mkdir(exist_ok=True, parents=True)
    url = CONFIG_URL + path.name
    try:
        res = requests.get(url, verify=ssl.CERT_NONE)
        with open(path, 'w', encoding='utf8') as fid:
            fid.write(res.text)
            logger.info(f'Config file "{path.name}" updated from {url}')
    except requests.exceptions.ConnectionError:
        logger.warning('Connection error. Could not update config files!')
        raise


def update_shape_files() -> None:
    SHAPE_FILES_DIR = TEMP_CONFIG_DIRECTORY / 'SHAPE_FILES'
    SHAPE_FILES_DIR.mkdir(exist_ok=True, parents=True)
    for name in SHAPE_FILES:
        target_path = SHAPE_FILES_DIR / name
        url = CONFIG_URL + 'SHAPE_FILES' + name
        try:
            # urllib.request.urlretrieve(url, target_path)

            res = requests.get(url, verify=ssl.CERT_NONE, stream=True)
            # with open(target_path, 'wb') as fid:
            #     fid.write(res.content)
            with open(target_path, 'wb') as fid:
                for chunk in res.iter_content(chunk_size=128):
                    fid.write(chunk)
            logger.info(f'Shapefile "{name}" updated from {url}')
        except requests.exceptions.ConnectionError:
            logger.warning(f'Connection error. Could not update shape file {name}')
            raise


def update_config_files() -> None:
    """Downloads config files from github"""
    for name in CONFIG_FILE_NAMES:
        target_path = TEMP_CONFIG_DIRECTORY / name
        update_config_file(target_path)


@functools.cache
def get_shape_file_info_at_position(x_pos: float, y_pos: float, variable: str) -> str | None:
    shape_file_obj = _get_shapefile_for_variable(variable)
    return shape_file_obj.get(x_pos=x_pos, y_pos=y_pos, variable=variable)


@functools.cache
def _get_shapefile_for_variable(variable: str, **kwargs) -> shape_files.ShapeFile:
    """Returns a shape_file.ShapeFile object that holds the given variable"""
    shape_file_config = shape_files.ShapeFilesConfig(get_config_path('shape_file_config.yaml'),
                                                     get_config_path('SHAPE_FILES'))
    path = shape_file_config.get_file_path_for_variable(variable)
    translation = shape_file_config.get_translations_for_file(path)
    obj = _get_shape_file_obj(path, **kwargs)
    obj.set_translation(translation)
    return obj


@functools.cache
def _get_shape_file_obj(path: pathlib.Path, **kwargs):
    return shape_files.ShapeFile(path, **kwargs)


if __name__ == '__main__':
    update_config_files()
