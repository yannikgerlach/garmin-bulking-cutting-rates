import json
import os
from datetime import date

import garminconnect

from scripts.files import RAW_DATA_FILE


def load_and_store_garmin_data():
    garmin = garminconnect.Garmin(
        os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD")
    )
    garmin.login()
    garmin.garth.dump(os.getenv("GARTH_HOME", "~/.garth"))

    startdate = os.getenv("GARMIN_START_DATE", None)
    if startdate is None:
        raise RuntimeError("Environment variable GARMIN_START_DATE is not set")
    enddate = date.today().isoformat()

    data = garmin.get_weigh_ins(startdate, enddate)
    if data is None:
        raise RuntimeError("Failed to retrieve data from Garmin")

    with open(RAW_DATA_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    load_and_store_garmin_data()
