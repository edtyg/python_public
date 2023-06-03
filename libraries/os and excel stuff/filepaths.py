import os 

# current file name
filename = os.path.basename(__file__)

# file full directory - including file name
full_path = os.path.realpath(__file__)

# folder of current file - does not include file name
full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

# list all the files that are in the current directory
print(os.listdir())

# os.mkdir("test") # creates a folder in current directory

# os.chdir('filepath...') # change current working directory to specified path

# os.remove("test.xlsx") # remove file