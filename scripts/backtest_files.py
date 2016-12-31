#!/usr/bin/python3

import json
import sys
from pprint import pprint
import requests
import re
import os
import shutil
import argparse
import glob

parser = argparse.ArgumentParser(description='Process backtesting')
parser.add_argument('--onefile', action='store_true')
parser.add_argument('config_name',nargs='?',default=None)
parser.add_argument('items',nargs='*')

args = parser.parse_args(sys.argv[1:])

location = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(location, "..", "data")

config_file = os.path.join(data_dir, args.config_name + ".json")
print("looking for ", config_file)

with open(config_file) as data_file:
	data = json.load(data_file)

if args.onefile:
	outfile = args.config_name + ".html"
	print("writing to ", outfile)
	with open(outfile, 'w') as outf:
		pass

for i in sorted(sum([glob.glob(i) for i in args.items], [])):
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
	if not args.onefile:
		outfile = args.config_name + '-' + k[0] + ".html"
		print("writing to ", outfile)
		with open(outfile, 'w') as outf:
			print(r.text, file=outf)
	else:
		outfile = args.config_name + ".html"
		print("writing to ", outfile)
		with open(outfile, 'a') as outf:
			print(r.text, file=outf)
