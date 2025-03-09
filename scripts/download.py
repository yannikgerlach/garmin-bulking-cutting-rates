import json
import os
from datetime import date

import garminconnect

from scripts.files import RAW_DATA_FILE


def get_start_date():
    startdate = os.getenv("GARMIN_START_DATE", None)
    if startdate is None:
        raise RuntimeError("Environment variable GARMIN_START_DATE is not set")

    try:
        return date.fromisoformat(startdate).isoformat()
    except ValueError as e:
        raise ValueError(
            f"Environment variable GARMIN_START_DATE is not in the correct format (YYYY-MM-DD): {e}"
        ) from e


def load_and_store_garmin_data():
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if email is None or password is None:
        raise RuntimeError(
            "Environment variables GARMIN_EMAIL and GARMIN_PASSWORD must be set"
        )

    garmin = garminconnect.Garmin(email, password)
    garmin.login()
    garmin.garth.dump(os.getenv("GARTH_HOME", "~/.garth"))

    startdate = get_start_date()
    enddate = date.today().isoformat()

    data = garmin.get_weigh_ins(startdate, enddate)
    if data is None:
        raise RuntimeError("Failed to retrieve data from Garmin")

    with open(RAW_DATA_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    load_and_store_garmin_data()
