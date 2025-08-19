import functools
import pathlib

from nodc_geography import bathymetry_db
from nodc_geography import location_db
from nodc_geography import shape_files
from nodc_geography import bathymetry
from nodc_geography.paths import get_config_path

@functools.cache
def get_bathymetry_depth_at_position(
        lat: float, lon: float
    ) -> float | None:

    depth = bathymetry_db.get(lat, lon)
    if depth:
        return depth
    depth, file_name = (
        bathymetry.get_emodnet_bathymetry_depth_and_source_name_at_position(lat, lon))
    if depth:
        bathymetry_db.add(lat, lon, depth, file_name)
    return depth


@functools.cache
def get_shape_file_info_at_position(
    x_pos: float, y_pos: float, variable: str
) -> str | None:
    db_name = location_db.get(x_pos, y_pos, variable)
    if db_name:
        return db_name
    shape_file_obj = _get_shapefile_for_variable(variable)
    name = shape_file_obj.get(x_pos=x_pos, y_pos=y_pos, variable=variable)
    if name:
        name = str(name)
        location_db.add(x_pos, y_pos, variable, name)
    return name


@functools.cache
def _get_shapefile_for_variable(variable: str, **kwargs) -> shape_files.ShapeFile:
    """Returns a shape_file.ShapeFile object that holds the given variable"""
    shape_file_config = shape_files.ShapeFilesConfig(
        get_config_path("shape_file_config.yaml"), get_config_path()
    )
    path = shape_file_config.get_file_path_for_variable(variable)
    translation = shape_file_config.get_translations_for_file(path)
    obj = _get_shape_file_obj(path, **kwargs)
    obj.set_translation(translation)
    return obj


@functools.cache
def _get_shape_file_obj(path: pathlib.Path, **kwargs):
    return shape_files.ShapeFile(path, **kwargs)


if __name__ == "__main__":
    info = get_shape_file_info_at_position(12.0, 57.0, "location_nation")
