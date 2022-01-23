"""
Lists the filename to be read in the main program (parser)
Requires the user to input the file name.
"""
import os
cur_path = os.path.dirname(__file__)

#Input file name OR use the current one
input_file = "UC1_CS_baseplate_subassembly_v001.bpmn"
new_path = os.path.relpath('..\\BPMN_files\\'+ input_file, cur_path) 
file_name = (cur_path +"/" + input_file).replace("/", "\\")
print(new_path)
print(cur_path)
print(file_name)