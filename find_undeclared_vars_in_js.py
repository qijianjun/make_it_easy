#coding: utf-8

# todo:
# remove regex /.*/
# detect var a=1,\nb=2\n...

import codecs
import re

with codecs.open("script.js", "r", "utf-8") as f:
	fc = f.read().strip()

functionPattern = re.compile(r'(function.*?)(?=\nfunction)', re.S)
functions = re.findall(functionPattern, fc)
for function in functions:
	# remove comments
	function = re.sub('\s+//.*?(?=\n)', '', function, re.M)
	function_name = re.findall(r'function (\w+)\(', function)
	all_args = re.findall(r'\((.*?)\)', function.split('\n')[0])[0].split(',')
	all_vars = re.findall(r'var .*', function)
	all_declared = []
	all_undeclared = []
	for arg in all_args:
		arg = arg.strip()
		if arg:
			all_declared.append(arg)
	for var in all_vars:
		var = var.replace('var ', '').replace(';', '')
		var = re.sub(r'\'.*?\'', '', var)
		var = re.sub(r'".*?"', '', var)
		commas = var.split(',')
		for comma in commas:
			var = comma.split('=')[0].strip()
			if var:
				all_declared.append(var)
	# remove quoted content
	nostr = re.sub(r'\'.*?\'', '', function)
	nostr = re.sub(r'".*?"', '', nostr)
	# collect
	# all_used = re.findall(r'\s+(\w+)\s*=', nostr)
	all_used = re.findall(r'\s+(\w+)\.', nostr)
	for used in all_used:
		# filter out the global vars
		if used not in all_declared and used not in all_undeclared and not re.match(r'[A-Z_]+', used) and used not in ['window', 'document', 'this', 'jQuery', 'console', 'location', 'event']:
			all_undeclared.append(used)
	if all_undeclared:
		try:
			print '===== ' + function_name[0] + ' ====='
		except:
			print '===== ====='
		print all_undeclared
