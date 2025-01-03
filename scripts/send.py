import base64
import os

import requests


def get_file_content_as_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


weight_plot_base64 = get_file_content_as_base64("weight.png")
weight_change_plot_base64 = get_file_content_as_base64("weight_change.png")

response = requests.post(
    os.environ["WEBHOOK_URL"],
    json={
        "weight_plot_base64": weight_plot_base64,
        "weight_change_plot_base64": weight_change_plot_base64,
    },
    headers={
        "x-api-key": os.getenv("MAKE_API_KEY"),
    },
    timeout=10,
)

print(response.text)
print(response.status_code)
