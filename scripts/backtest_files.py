#!/usr/bin/python3

import json
import sys
from pprint import pprint
import requests
import re
import os
import shutil

location = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(location, "..", "data")

config_name = sys.argv[1]
items = sys.argv[2:]
config_file = os.path.join(data_dir, config_name + ".json")
print("looking for ", config_file)

with open(config_file) as data_file:
	data = json.load(data_file)

for i in items:
	base_name = os.path.basename(i)
	data_file = os.path.join(data_dir, base_name)
	if os.path.exists(data_file):
		print(i, " already exists in data dir", data_dir)
	else:
		print("copying ", i, " to ", data_dir)		       
		shutil.copy(i, data_file)
	data['tickersource'] = base_name
	r = requests.post("http://localhost:5000/backtest",
			  data)
	k = base_name.rsplit(".", 1)
	outfile = k[0] + ".html"
	print("writing to ", outfile)
	with open(outfile, 'w') as outf:
		print(r.text, file=outf)
