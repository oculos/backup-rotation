import os
import json
from datetime import datetime

backup_dir = ""
max_size = 0
files = []
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
        attr['size'] = os.path.getsize(attr["full_path"])
        attr['created'] = os.path.getctime(attr['full_path'])
        files.append(attr)   
    for dire in directories:
        list_files(os.path.join(path,dire))
    
    
list_files(backup_dir)
files = sorted(files, key = lambda k: k['created'])
size = sum(item['size'] for item in files) 
print "Before: "+str(size) 
while size > max_size:
    del_fil = files.pop(0)
    size = size - del_fil['size']
    os.remove(del_fil['full_path'])
print files
print "After: "+str(sum(item['size'] for item in files)) 