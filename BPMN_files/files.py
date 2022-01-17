"""
Lists the filename to be read in the main program (parser)
Requires the user to input the file name.
"""
import os

#Input file name OR use the current one
input_file = "UC1_CS_baseplate_subassembly_v001.bpmn"
 
files_dir = os.getcwd()
file_name = str(files_dir +"\\" + input_file)


