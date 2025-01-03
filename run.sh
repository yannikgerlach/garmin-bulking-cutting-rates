# run download, plot and process after another (using poetry environment)
# Usage: ./run.sh

poetry run python scripts/download.py
poetry run python scripts/process.py
poetry run python scripts/plot.py
poetry run python scripts/send.py
