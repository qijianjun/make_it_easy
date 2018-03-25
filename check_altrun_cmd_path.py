#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re

with codecs.open("ShortCutList.txt", "r", "gbk") as f:
	lines = f.readlines()
new = ""
drop = ""
for line in lines:
	path = line.split("|")[-1].strip().strip("\"")
	path = re.sub(r'(?P<ext>\.(exe|cmd|bat)).*', "\g<ext>", path)
	if path.find(":\\") != -1 and not os.path.exists(path):
		print path.encode("gbk", "ignore")
		drop += line
		continue
	new += line
with codecs.open("ShortCutList-new.txt", "w", "gbk") as f:
	f.write(new)
with codecs.open("ShortCutList-drop.txt", "w", "gbk") as f:
	f.write(drop)
