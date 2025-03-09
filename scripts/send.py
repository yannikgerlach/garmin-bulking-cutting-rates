import base64
import os

import requests

from scripts.files import REMAINING_DAYS_WEIGHT_PNG, WEIGHT_CHANGE_PNG, WEIGHT_PNG


def get_file_content_as_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def send(text: str = "") -> None:
    """
    Send weight analysis data to a webhook endpoint.
    This function encodes three weight-related plots as base64 strings and sends them
    along with provided text to a webhook URL specified in the environment variables.

    Args:
        text (str, optional): Additional text information about weight to include in the payload.
    """

    weight_plot_base64 = get_file_content_as_base64(WEIGHT_PNG)
    weight_change_plot_base64 = get_file_content_as_base64(WEIGHT_CHANGE_PNG)
    remaining_days_weight_plot_base64 = get_file_content_as_base64(
        REMAINING_DAYS_WEIGHT_PNG
    )

    response = requests.post(
        os.environ["WEBHOOK_URL"],
        json={
            "weight_plot_base64": weight_plot_base64,
            "weight_change_plot_base64": weight_change_plot_base64,
            "remaining_days_weight_plot_base64": remaining_days_weight_plot_base64,
            "weight_text": text,
        },
        headers={
            "x-api-key": os.getenv("MAKE_API_KEY"),
        },
        timeout=10,
    )

    print(response.text)
    print(response.status_code)


if __name__ == "__main__":
    send()
