"""
Lists the filename to be read in the main program (parser)
Requires the user to input the file name.
"""
import os

#Input file name OR use the current one
input_file = "Basicexample.bmpn"
 
files_dir = os.getcwd()
print()
file_name = str(files_dir +"\\" + input_file)


