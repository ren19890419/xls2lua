#! /usr/bin/env python
# -*- coding: utf-8 -*
# author: luzexi

import xlrd
import os.path
import time
import os
import codecs
import re

SCRIPT_HEAD = "-- this fight_value_normal_table is generated by program!\n\
-- don't change it manaully. by rensiwei\n\
-- source file: %s\n\
-- created at: %s\n\
\n\
"

def make_table(filename):
	if not os.path.isfile(filename):
		raise NameError, "%s is	not	a valid	filename" % filename
	# book_xlrd = xlrd.open_workbook(filename,formatting_info=True)
	book_xlrd = xlrd.open_workbook(filename)

	excel = {}
	excel["filename"] = filename
	excel["data"] = {}
	for sheet in book_xlrd.sheets():
		sheet_name = sheet.name.replace(" ", "_")
		excel["data"][sheet_name] = {}
		row_idx = 0
		for row_idx in xrange(sheet.nrows):
			row = {}
			col_idx = 0
			for col_idx in xrange(sheet.ncols):
				value = sheet.cell_value(row_idx, col_idx)
				vtype = sheet.cell_type(row_idx, col_idx)
				v = None
				if 0 == row_idx:
					v = format_str(value)
				elif vtype == 2:
					v = int(value)
				row[col_idx] = v
			excel["data"][sheet_name][row_idx] = row
	return excel, 0 , "ok"

def format_str(v):
	if type(v) == int or type(v) == float :
		v =  bytes(v)
	s = ("%s"%(""+v)).encode("utf-8")
	s = s.replace('\"','\\\"')
	s = s.replace('\'','\\\'')
	return s
	
def get_s(v):
	if v is None:
		return ""
	return v

def write_to_help_otherconf_script(output_path,input_filename, output_filename):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	infp = codecs.open(output_path + "/" + input_filename + ".lua", 'r+','utf-8')
	outfp = codecs.open(output_path + "/" + output_filename + ".lua", 'r+','utf-8')
	in_lines = infp.readlines()
	in_flen=len(in_lines)-1
	out_lines = outfp.readlines()
	out_flen=len(out_lines)-1
	search_line = -1
	for j in range(out_flen):
		if in_lines[0] == out_lines[j]:
			search_line = j
			break
	if -1 != search_line and search_line < out_flen:
		#print search_line
		for i in range(in_flen+1):
			out_lines[search_line + i] = in_lines[i]
	codecs.open(output_path + "/" + output_filename + ".lua", 'w+','utf-8').writelines(out_lines)
	#outfp.writelines(out_lines)
	outfp.close()
	infp.close()
	
def write_to_lua_script(excel, output_path):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	for (sheet_name, sheet) in excel["data"].items():
		outfp = open(output_path + "/" + sheet_name + ".lua", 'w+')
		create_time = time.strftime("%a %b %d %H:%M:%S %Y", time.gmtime(time.time()))
		outfp.write(SCRIPT_HEAD % (excel["filename"], create_time)) 
		outfp.write("fight_value_normal = \n")
		outfp.write("{\n")
		for (row_idx, row) in sheet.items():
			if 0 == row_idx:
				outfp.write("--[ " + '%1s'%str(row_idx) + "] = {")
			else:
				outfp.write("[" + '%3s'%str(row_idx) + "] = {")
			field_index = 0
			for (col_idx, field)in row.items():
				if 0 == col_idx:
					continue
				if field_index > 0:
					outfp.write(",")
				field_index += 1
				tmp_str = get_s(row[col_idx])
				if 0 == row_idx:
					for write_space in range(2,12-len(tmp_str)):
						outfp.write(" ")
					outfp.write('%s'%tmp_str)
				else:
					outfp.write('%8s'%tmp_str)
			outfp.write("},\n")
			
		outfp.write("\n}\n")
		#outfp.write("\nreturn fight_value_normal\n")
		outfp.close()
		
def main():
	import sys
	if len(sys.argv) < 3:
		sys.exit('''usage: xls2lua.py excel_name output_path''')
	filename = sys.argv[1]
	output_path = sys.argv[2]
	if not os.path.exists(filename):
		sys.exit("error: "+filename+" is not exists.")
	t, ret, errstr = make_table(filename)
	if ret != 0:
		print(filename)
		print "error: " + errstr
	else:
		print(filename)
		print "res:"
		# print(t)
		print "success!!!"
	write_to_lua_script(t, output_path)
	write_to_help_otherconf_script(output_path,"Sheet1","help_otherconf")
if __name__=="__main__":
	main()