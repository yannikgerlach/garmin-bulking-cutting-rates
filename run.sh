#!/bin/bash

poetry run python scripts/download.py
poetry run python scripts/process.py
if [ "$1" == "--send" ]; then
    poetry run python scripts/send.py
fi
