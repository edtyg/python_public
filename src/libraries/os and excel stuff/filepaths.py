import os

# current file name
filename = os.path.basename(__file__)
print(f"filename: {filename}")

# file full directory - including file name
full_path = os.path.realpath(__file__)
print(f"fullpath: {full_path}")

# folder of current file - does not include file name
save_path = os.path.dirname(os.path.realpath(__file__))
print(f"savepath: {save_path}")

# list all the files that are in the current directory
list_files = os.listdir()
print(f"list of files in current folder: {list_files}")

# os.mkdir("test") # creates a folder in current directory
# os.chdir('filepath...') # change current working directory to specified path
# os.remove("test.xlsx") # remove file
