import os
import json
from datetime import datetime

backup_dir = ""
max_size = 0
files = []
deleted_files = []

with open("settings.json","r") as settings:
    js = json.load(settings)
    backup_dir = js['backup_dir']
    max_size = js['max_storage']

if backup_dir == "": 
    print ("Please configure which directory to work on.")
    exit(1)
    
def list_files(path):
    global files
    all_files = os.listdir(path)
    just_files = [x for x in all_files if os.path.isfile(os.path.join(path,x))]
    directories = [x for x in all_files if os.path.isdir(os.path.join(path,x)) and not os.path.islink(os.path.join(path,x))]
    
    for fil in just_files:
        attr = {}
        attr['full_path'] = os.path.join(path,fil)
        attr['path'] = path
        attr['name'] = fil
        attr['size'] = os.path.getsize(attr["full_path"])
        attr['created'] = os.path.getctime(attr['full_path'])
        files.append(attr)   
    for dire in directories:
        list_files(os.path.join(path,dire))
    
    
list_files(backup_dir)
files = sorted(files, key = lambda k: k['created'])
size = sum(item['size'] for item in files) 
deleted = False
while size > max_size:
    deleted = True
    del_fil = files.pop(0)
    deleted_files.append(del_fil)
    size = size - del_fil['size']
    os.remove(del_fil['full_path'])

if deleted:
    with open("deleted.log","a") as f:
        date = str(datetime.now()).split('.')[0]
        f.write(date+' [INFO] '+str(len(deleted_files))+' files deleted, '+str(sum(item['size'] for item in deleted_files))+' bytes free\'d. Current used space on directory: '+str(size)+' bytes. Below is the list of deleted files:\n')
        for fil in deleted_files:
            f.write('\t- '+fil['name']+' from '+fil['path']+"\n")