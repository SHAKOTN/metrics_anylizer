import json
import os
from typing import Dict
from typing import List


def read_metrics() -> List[Dict]:
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "producer",
        "packages.json"
    )
    with open(path) as file:
        data = json.load(file)
    return data
