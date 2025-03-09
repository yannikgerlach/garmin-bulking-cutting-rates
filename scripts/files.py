import os


def get_storage_directory_env() -> str:
    """
    Returns the storage directory path from the environment variable STORAGE_DIRECTORY.
    If the environment variable is not set, it defaults to "./".
    """
    return os.getenv("STORAGE_DIRECTORY", "./")


def get_storage_directory() -> str:
    directory_path = get_storage_directory_env()
    if not os.path.isdir(directory_path):
        raise RuntimeError(
            f"Storage directory {directory_path} does not exist or is not a directory."
        )
    if not os.access(directory_path, os.R_OK | os.W_OK):
        raise RuntimeError(
            f"Storage directory {directory_path} is not readable or writable."
        )
    return directory_path


def get_full_storage_path(filename: str) -> str:
    return os.path.join(get_storage_directory(), filename)


storage_directory = get_storage_directory()

RAW_DATA_FILE = os.path.join(storage_directory, "weight_raw.json")
DAILY_DATA_FILE = os.path.join(storage_directory, "weight_daily.csv")
WEEKLY_DATA_FILE = os.path.join(storage_directory, "weight.csv")

WEIGHT_CHANGE_PNG = os.path.join(storage_directory, "weight_change.png")
WEIGHT_PNG = os.path.join(storage_directory, "weight.png")
REMAINING_DAYS_WEIGHT_PNG = os.path.join(storage_directory, "remaining_days_weight.png")
