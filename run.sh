#!/bin/bash

poetry run python scripts/download.py
poetry run python scripts/process.py --send
