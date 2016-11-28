#!/usr/bin/python3

import json
import sys
from pprint import pprint
import requests

with open(sys.argv[1]) as data_file:
        data = json.load(data_file)
        r = requests.post("http://localhost:5000/backtest",
                          data)
        print(r.text)
