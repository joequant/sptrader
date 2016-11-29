#!/usr/bin/python3

import json
import sys
from pprint import pprint
import requests
import re
import os

for i in sys.argv[1:]:
	if re.search('\.json$', i):
		with open(i) as data_file:
			data = json.load(data_file)
			r = requests.post("http://localhost:5000/backtest",
					  data)
			outfile = re.sub('\.json$', '.html',
					 os.path.basename(i))
			print("writing to ", outfile)
			with open(outfile, 'w') as outf:
				print(r.text, file=outf)
