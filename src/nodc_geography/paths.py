import os
import pathlib


def get_user_given_config_dir() -> pathlib.Path | None:
    path = pathlib.Path(os.getcwd()) / "config_directory.txt"
    if not path.exists():
        return
    with open(path) as fid:
        config_path = fid.readline().strip()
        if not config_path:
            return
        config_path = pathlib.Path(config_path)
        if not config_path.exists():
            return
        return config_path


CONFIG_ENV = "NODC_CONFIG"

home = pathlib.Path.home()
OTHER_CONFIG_SOURCES = [
    home / "NODC_CONFIG",
    home / ".NODC_CONFIG",
    home / "nodc_config",
    home / ".nodc_config",
]

CONFIG_SUBDIRECTORY = "sharkweb_shapefiles"
CONFIG_FILE_NAMES = ["shape_file_config.yaml"]

SHAPE_FILES = [
    "1 Shapefile-översikt.txt",
    "ak_riks.cpg",
    "ak_riks.dbf",
    "ak_riks.prj",
    "ak_riks.qix",
    "ak_riks.shp",
    "ak_riks.shx",
    "an_riks.cpg",
    "an_riks.dbf",
    "an_riks.prj",
    "an_riks.qix",
    "an_riks.shp",
    "an_riks.shx",
    "havdirtyper_2012_delatKattegatt.dbf",
    "havdirtyper_2012_delatKattegatt.prj",
    "havdirtyper_2012_delatKattegatt.qix",
    "havdirtyper_2012_delatKattegatt.sbn",
    "havdirtyper_2012_delatKattegatt.sbx",
    "havdirtyper_2012_delatKattegatt.shp",
    "havdirtyper_2012_delatKattegatt.shp.xml",
    "havdirtyper_2012_delatKattegatt.shx",
    "Havsomr_SVAR_2016_3b_CP1252.dbf",
    "Havsomr_SVAR_2016_3b_CP1252.qix",
    "Havsomr_SVAR_2016_3b_CP1252.shp",
    "Havsomr_SVAR_2016_3b_CP1252.shx",
    "Havsomr_SVAR_2016_3c_CP1252.dbf",
    "Havsomr_SVAR_2016_3c_CP1252.qix",
    "Havsomr_SVAR_2016_3c_CP1252.shp",
    "Havsomr_SVAR_2016_3c_CP1252.shx",
    "havsomr_y_2012_2.dbf",
    "havsomr_y_2012_2.prj",
    "havsomr_y_2012_2.qix",
    "havsomr_y_2012_2.sbn",
    "havsomr_y_2012_2.sbx",
    "havsomr_y_2012_2.shp",
    "havsomr_y_2012_2.shp.xml",
    "havsomr_y_2012_2.shx",
    "KOMMUNER_LAN.dbf",
    "KOMMUNER_LAN.prj",
    "KOMMUNER_LAN.qix",
    "KOMMUNER_LAN.sbn",
    "KOMMUNER_LAN.sbx",
    "KOMMUNER_LAN.shp",
    "KOMMUNER_LAN.shp.xml",
    "KOMMUNER_LAN.shx",
    "KONVENTION.dbf",
    "KONVENTION.prj",
    "KONVENTION.qix",
    "KONVENTION.sbn",
    "KONVENTION.sbx",
    "KONVENTION.shp",
    "KONVENTION.shx",
    "MSFD_areas.dbf",
    "MSFD_areas.prj",
    "MSFD_areas.qix",
    "MSFD_areas.sbn",
    "MSFD_areas.sbx",
    "MSFD_areas.shp",
    "MSFD_areas.shp.xml",
    "MSFD_areas.shx",
    "MSFD_areas_TM.dbf",
    "MSFD_areas_TM.prj",
    "MSFD_areas_TM.qpj",
    "MSFD_areas_TM.shp",
    "MSFD_areas_TM.shx",
]


CONFIG_DIRECTORY = None
conf_dir = get_user_given_config_dir()
if conf_dir:
    CONFIG_DIRECTORY = conf_dir / CONFIG_SUBDIRECTORY
else:
    if os.getenv(CONFIG_ENV) and pathlib.Path(os.getenv(CONFIG_ENV)).exists():
        CONFIG_DIRECTORY = pathlib.Path(os.getenv(CONFIG_ENV)) / CONFIG_SUBDIRECTORY
    else:
        for directory in OTHER_CONFIG_SOURCES:
            if directory.exists():
                CONFIG_DIRECTORY = directory / CONFIG_SUBDIRECTORY
                break


def get_config_path(name: str = None) -> pathlib.Path:
    if not CONFIG_DIRECTORY:
        raise NotADirectoryError(
            f"Config directory not found. Environment path {CONFIG_ENV} does not seem to be set and not other config directory was found. "
        )
    if not name:
        return CONFIG_DIRECTORY
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    path = CONFIG_DIRECTORY / name
    if not path.exists():
        raise FileNotFoundError(f"Could not find config file {name}")
    return path
