import functools
import pathlib

from shapely import Point

from nodc_geography import bathymetry_db
from nodc_geography import location_db
from nodc_geography import shape_files
from nodc_geography import bathymetry
from nodc_geography.paths import get_config_path


# @functools.cache
# def get_bathymetry_depth_at_position(
#         lat: float, lon: float
#     ) -> float | None:
#
#     depth = bathymetry_db.get(lat, lon)
#     if depth is not None:
#         return -depth
#     info = (
#         bathymetry.get_emodnet_bathymetry_info_at_position(lat, lon))
#     if info:
#         info["match_lat"] = info["lat"]
#         info["match_lon"] = info["lon"]
#         info["lat"] = lat
#         info["lon"] = lon
#         bathymetry_db.add(**info)
#     return -info["z"]


@functools.cache
def get_bathymetry_depth_at_position(
        lat: float, lon: float
    ) -> dict:

    info = bathymetry_db.get(lat, lon)
    if info is not None:
        return info
    info = bathymetry.get_emodnet_bathymetry_info_at_position(lat, lon)
    if info:
        info["match_lat"] = info["lat"]
        info["match_lon"] = info["lon"]
        info["lat"] = lat
        info["lon"] = lon
        bathymetry_db.add(**info)
    return info


# @functools.cache
# def get_shape_file_info_at_position(
#     x_pos: float, y_pos: float, variable: str
# ) -> str | None:
#     db_name = location_db.get(x_pos, y_pos, variable)
#     if db_name:
#         return db_name
#     shape_file_obj = _get_shapefile_for_variable(variable)
#     name = shape_file_obj.get(x_pos=x_pos, y_pos=y_pos, variable=variable)
#     if name:
#         name = str(name)
#         location_db.add(x_pos, y_pos, variable, name)
#     return name

# @functools.cache
# def get_shape_file_info_at_position(
#     x_pos: float, y_pos: float, variable: str
# ) -> str | None:
#     db_name = location_db.get(x_pos, y_pos, variable)
#     if db_name:
#         return db_name
#     shape_file_obj = _get_shapefile_for_variable(variable)
#     info = shape_file_obj.get_all(x_pos=x_pos, y_pos=y_pos, variable=variable)
#     x = []
#     y = []
#     va = []
#     na = []
#     if info:
#         for var, name in info.items():
#             x.append(x_pos)
#             y.append(y_pos)
#             va.append(var)
#             na.append(name)
#         location_db.add_multiple(x, y, va, na)
#     return info.get(variable)


@functools.cache
def get_shape_file_info_at_position(
    x_pos: float, y_pos: float, variable: str) -> dict[str, str]:
    db_info = location_db.get_all_for_position(x_pos, y_pos)
    if db_info.get(variable):
        return db_info
    shape_file_obj = _get_shapefile_for_variable(variable)
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
    # variable = "location_rg"
    variable = "location_sea_area_code"
    x_pos = 610641
    y_pos = 6825175


    # obj = _get_shapefile_for_variable("location_sea_area_code")

    # info_var = location_db.get(x_pos, y_pos, variable)
    # info = location_db.get_all_for_position(x_pos, y_pos)
    #
    # shape_file_config = shape_files.ShapeFilesConfig(
    #     get_config_path("shape_file_config.yaml"), get_config_path()
    # )
    # obj = _get_shapefile_for_variable(variable)
    #
    # boolean = obj._gdf.contains(Point(x_pos, y_pos))
    # translated_variable = obj._translation.get(variable)
    #
    # name = obj.get(x_pos, y_pos, variable)
    #
    #
    info = get_shape_file_info_at_position(x_pos, y_pos, variable)
