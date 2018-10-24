import json
import requests
import os
import logging
from datetime import datetime

start = datetime.utcnow()

with open("crawl_config.json", "r") as f:
    config = json.load(f)

directory = config["path"] + datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

if not os.path.exists(directory):
    os.makedirs(directory)

LOG_FILENAME = directory + "/" + "crawl.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

logging.debug("Crawling "+str(len(config["source"])) + " source(s)")

for i, uri in enumerate(config["source"]):
    response = requests.get(uri)
    if response.raise_for_status() == None:
        file_name = os.path.join(directory, str(i) + "." + "rss")
        with open(file_name, "w") as f:
            f.write(response.text)

end = datetime.utcnow()

logging.debug("Runtime: " + str(end-start))
