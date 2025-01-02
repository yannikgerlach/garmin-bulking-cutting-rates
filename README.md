# Garmin Weight Analysis for Bulking and Cutting
Applications like Garmin Connect provide various analysis tools for your weight data.
However, these tools are limited in the time range they can display.
For example, Garmin Connect can only display the weight average for the last day, 7 days, 4 weeks and year.
As a result, it's unsuitable for effectively comparing your weight change to optimal [bulking rates](https://macrofactorapp.com/bulking-calculator/) or [cutting rates](https://macrofactorapp.com/cutting-calculator/).

The code calculates weekly and two-weekly averages of the weight data.
It also calculates the weight change per week based on the weekly and two-weekly averages, respectively.
You can use these to more accurately track your weight over time,
spotting trends and changes more easily and smoothing out daily fluctuations.

This repository contains code for analyzing your Garmin weight data in a more flexible way.
The weight data gets loaded with the [garminconnect](https://pypi.org/project/garminconnect/) package.
The data is then analysed with the [pandas](https://pandas.pydata.org/) package.

## Installation
This repository uses poetry for dependency management.
To install the dependencies, run the following command:
```bash
poetry install
```

## Usage
You need a Garmin account with weight data to use this repository.

To use the code, you need to create a `.env` file in the root directory of this repository.
The `.env` file should contain the following variables:
```bash
GARMIN_USERNAME=<your_garmin_username>
GARMIN_PASSWORD=<your_garmin_password>
```

After creating the `.env` file, you can run the code with the following command to downloaded the weight data:
```bash
poetry run python scripts/download.py
```

This stores the weight data in a file called `weight.json`.

Using this data, you can then process the weight data with the following command:
```bash
poetry run python scripts/process.py
```

This stores the processed weight data in a file called `weight.csv`.

You can then plot the data with the following command:
```bash
poetry run python scripts/plot.py
```

You can specify your targeted weekly weight change rate for bulking (positive) or cutting (negative) in the `.env` file:
```bash
TARGET_WEEKLY_CHANGE_PERCENTAGE=<your_targeted_weekly_change_percentage>
```

For example, if you want to gain 0.5% of your body weight per week, you can set the following variable:
```bash
TARGET_WEEKLY_CHANGE_PERCENTAGE=0.005
```

To run everything in one go, you can use the following command:
```terminal
/bin/bash run.sh
```
