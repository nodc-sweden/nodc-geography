import functools
import pathlib

from nodc_config import Config

from nodc_geography import location_db, shape_files
from nodc_geography.paths import get_config_directory, get_config_path


@functools.cache
def get_shape_file_info_at_position(
    nodc_conf: Config, x_pos: float, y_pos: float, variable: str
) -> dict[str, str]:
    db_info = location_db.get_all_for_position(x_pos, y_pos)
    if db_info.get(variable):
        return db_info
    shape_file_obj = _get_shapefile_for_variable(nodc_conf, variable)
    info = shape_file_obj.get_all(x_pos=x_pos, y_pos=y_pos, variable=variable)
    x = []
    y = []
    va = []
    na = []
    if info:
        for var, name in info.items():
            x.append(x_pos)
            y.append(y_pos)
            va.append(var)
            na.append(name)
        location_db.add_multiple(x, y, va, na)
        db_info.update(info)
    return db_info


@functools.cache
def _get_shapefile_for_variable(
    nodc_conf: Config, variable: str, **kwargs
) -> shape_files.ShapeFile:
    """Returns a shape_file.ShapeFile object that holds the given variable"""
    shape_file_config = shape_files.ShapeFilesConfig(
        get_config_path(nodc_conf, "shape_file_config.yaml"),
        get_config_directory(nodc_conf, "sharkweb_shapefiles"),
    )
    path = shape_file_config.get_file_path_for_variable(variable)
    translation = shape_file_config.get_translations_for_file(path)
    obj = _get_shape_file_obj(path, **kwargs)
    obj.set_translation(translation)
    return obj


@functools.cache
def _get_shape_file_obj(path: pathlib.Path, **kwargs):
    return shape_files.ShapeFile(path, **kwargs)


def clear_cache():
    get_shape_file_info_at_position.cache_clear()
    _get_shapefile_for_variable.cache_clear()
    _get_shape_file_obj.cache_clear()
