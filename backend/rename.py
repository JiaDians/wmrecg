import os

directory_path = 'wm_mature'
file_name_list = os.listdir(directory_path)

for file in file_name_list:
    src = directory_path + '/' + file
    dst = directory_path + '/' + file[3:]
    os.rename(src, dst)

