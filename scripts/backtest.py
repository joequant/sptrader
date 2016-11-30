#!/usr/bin/python3

import json
import sys
from pprint import pprint
import requests
import re
import os

config_file = sys.argv[1]
items = sys.argv[2:]
with open(config_file) as data_file:
	data = json.load(data_file)

for k, v in data['backtest_data'].items():
	for i in items:
		if k.startswith(i):
			print("loading configuration", k)
			r = requests.post("http://localhost:5000/backtest",
					  v)
			outfile = k + ".html"
			print("writing to ", outfile)
			with open(outfile, 'w') as outf:
				print(r.text, file=outf)
