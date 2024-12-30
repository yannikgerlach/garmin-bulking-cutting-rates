from datetime import date
import os
import pandas as pd
import json

import garminconnect


garmin = garminconnect.Garmin(os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD"))
garmin.login()

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)


startdate = date(2024, 11, 1)
startdate = startdate.isoformat()

enddate = date.today()
enddate = enddate.isoformat()

data = garmin.get_weigh_ins(startdate, enddate)
assert data is not None

with open("weight_raw.json", "w") as f:
    f.write(json.dumps(data))
