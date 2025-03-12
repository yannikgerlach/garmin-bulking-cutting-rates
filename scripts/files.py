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


RAW_DATA_FILE = get_full_storage_path("weight.json")

WEIGHT_CHANGE_PNG = get_full_storage_path("weight_change.png")
WEIGHT_PNG = get_full_storage_path("weight.png")
REMAINING_DAYS_WEIGHT_PNG = get_full_storage_path("remaining_days_weight.png")
