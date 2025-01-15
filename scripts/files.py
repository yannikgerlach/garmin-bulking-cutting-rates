import os


def get_storage_directory_env() -> str:
    return os.getenv("STORAGE_DIRECTORY", "./")


def get_storage_directory() -> str:
    storage_directory = get_storage_directory_env()
    if not os.path.exists(storage_directory):
        raise RuntimeError(f"Storage directory {storage_directory} does not exist.")
    if not os.access(storage_directory, os.R_OK):
        raise RuntimeError(f"Storage directory {storage_directory} is not readable.")
    return storage_directory


def get_full_storage_path(filename: str) -> str:
    return os.path.join(get_storage_directory(), filename)


RAW_DATA_FILE = get_full_storage_path("weight_raw.json")
DAILY_DATA_FILE = get_full_storage_path("weight_daily.csv")
WEEKLY_DATA_FILE = get_full_storage_path("weight.csv")

WEIGHT_CHANGE_PNG = get_full_storage_path("weight_change.png")
WEIGHT_PNG = get_full_storage_path("weight.png")
