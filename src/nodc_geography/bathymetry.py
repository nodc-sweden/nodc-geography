import polars as pl
import pathlib
import functools
from nodc_geography.paths import BATHYMETRY_DIRECTORY


def _get_emodnet_bathymetry_file_path_for_position(
            directory: pathlib.Path,
            lat: float,
            lon: float
        ) -> pathlib.Path | None:
    for path in directory.iterdir():
        if not path.name.startswith("emodnet_bathymetry"):
            continue
        try:
            parts = path.stem.split("-")
            lat_min, lat_max, lon_min, lon_max = map(float, parts[1:])
            if (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max):
                return path
        except ValueError:
            continue


@functools.cache
def _get_polars_dataframe_for_emodnet_bathymetry(path: pathlib.Path) -> pl.DataFrame:
    return pl.read_csv(path, separator=";")


def _get_emodnet_bathymetry_info_at_position_in_file(path: pathlib.Path,
                                                     lat: float,
                                                     lon: float) -> dict | None:
    if not path:
        raise FileNotFoundError
    df = _get_polars_dataframe_for_emodnet_bathymetry(path)
    df = df.with_columns(
        abs_lat_diff=(pl.col("lat") - lat).abs(),
        abs_lon_diff=(pl.col("lon") - lon).abs()
    )

    df_filtered = (
        df.lazy()
        .with_columns(
            abs_lat_diff=(pl.col("lat") - lat).abs(),
            abs_lon_diff=(pl.col("lon") - lon).abs()
        )
        .filter(
            pl.col.abs_lat_diff == pl.col.abs_lat_diff.min()
        )
        .filter(
            pl.col.abs_lon_diff == pl.col.abs_lon_diff.min(),
        ).collect()
    )
    return df_filtered.to_dicts()[0]


def get_emodnet_bathymetry_depth_at_position(lat: float,
                                             lon: float) -> float | None:
    path = _get_emodnet_bathymetry_file_path_for_position(
        directory=BATHYMETRY_DIRECTORY,
        lat=lat, lon=lon
    )
    result = _get_emodnet_bathymetry_info_at_position_in_file(
        path, lat, lon
    )
    if not result:
        return result
    return result["z"]


def get_emodnet_bathymetry_info_at_position(lat: float,
                                            lon: float) -> dict:
    path = _get_emodnet_bathymetry_file_path_for_position(
        directory=BATHYMETRY_DIRECTORY,
        lat=lat, lon=lon
    )
    result = _get_emodnet_bathymetry_info_at_position_in_file(
        path, lat, lon
    )
    if not result:
        return {}
    result["source_file_name"] = path.name
    return result


def rename_emodnet_bathymetry_xyz_files(directory: str):
    import re
    root = pathlib.Path(directory)
    for path in root.iterdir():
        if not re.match(r"\D\d_\d{4}.xyz", path.name):
            continue
        print(f"Renaming file: {path}")
        df = pl.read_csv(path, separator=";", new_columns=["lon", "lat", "z"],
                         has_header=False)

        lat_min = df.select(pl.col("lat").min())["lat"][0]
        lat_max = df.select(pl.col("lat").max())["lat"][0]

        lon_min = df.select(pl.col("lon").min())["lon"][0]
        lon_max = df.select(pl.col("lon").max())["lon"][0]

        new_name = f"emodnet_bathymetry-{lat_min}-{lat_max}-{lon_min}-{lon_max}.xyz"

        df = df[["lat", "lon", "z"]]

        df.write_csv(path.parent / new_name, separator=";")


if __name__ == "__main__":
    rename_emodnet_bathymetry_xyz_files(r"C:\mw\git\nodc_config\bathymetry")
    # dd = get_emodnet_bathymetry_depth_at_position(55.3, 15)
    # print(dd)


