import json
import os
from datetime import date

import garminconnect

garmin = garminconnect.Garmin(os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD"))
garmin.login()

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)

startdate = date(2024, 11, 1).isoformat()  # to do: allow user to specify start date
enddate = date.today().isoformat()

data = garmin.get_weigh_ins(startdate, enddate)
assert data is not None

with open("weight_raw.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(data))
