import functools
import pathlib

from nodc_geography import shape_files

THIS_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = THIS_DIR / 'CONFIG_FILES'


shape_file_config = shape_files.ShapeFilesConfig(CONFIG_DIR / 'shape_file_config.yaml')


@functools.cache
def get_shape_file_info_at_position(x_pos: float, y_pos: float, variable: str) -> str | None:
    shape_file_obj = _get_shapefile_for_variable(variable)
    return shape_file_obj.get(x_pos=x_pos, y_pos=y_pos, variable=variable)


@functools.cache
def _get_shapefile_for_variable(variable: str, **kwargs) -> shape_files.ShapeFile:
    """Returns a shape_file.ShapeFile object that holds the given variable"""
    path = shape_file_config.get_file_path_for_variable(variable)
    translation = shape_file_config.get_translations_for_file(path)
    obj = _get_shape_file_obj(path, **kwargs)
    obj.set_translation(translation)
    return obj


@functools.cache
def _get_shape_file_obj(path: pathlib.Path, **kwargs):
    return shape_files.ShapeFile(path, **kwargs)


if __name__ == '__main__':
    name = get_shape_file_info_at_position(x_pos=897525.051, y_pos=7323117.602, variable='location_water_district')
    print(name)
    name = get_shape_file_info_at_position(x_pos=897525.051, y_pos=7323117.602, variable='location_county')
    print(name)
