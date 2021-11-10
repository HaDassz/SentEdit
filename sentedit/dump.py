#!/usr/bin/python3

import json,sys

T=json.load(open(sys.argv[1]))

for k,v in T.items():
	print("%s\t%s"%(k,v))
