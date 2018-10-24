import json
import requests
import os
from datetime import datetime

with open("crawl_config.json", "r") as f:
    config = json.load(f)

print(config["source"])

directory = config["path"] + datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

if not os.path.exists(directory):
    os.makedirs(directory)

for i, uri in enumerate(config["source"]):
    response = requests.get(uri)
    if response.raise_for_status() == None:
        file_name = os.path.join(directory, str(i) + "." + "rss")
        with open(file_name, "w") as f:
            f.write(response.text)
