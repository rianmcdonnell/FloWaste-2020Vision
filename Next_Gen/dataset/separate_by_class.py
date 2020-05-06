"""
Relevant Files:
classes-segmentable.csv: convert from class name to real name
train-labels.csv: convert from ID to class
"""
import csv, os, glob, re, sys

mode = sys.argv[1]
path = './data_v6/'

# Parameters
class_file = './classes-segmentable.csv'
label_file = f'{path}{mode}-parsed-labels.csv'
base_dir = f'{path}{mode}/'

if not os.path.exists(base_dir+'images/'):
    os.mkdir(base_dir+'images/')


# Make class id->name converter
class_lookup = {}
with open(class_file) as f:
    reader = csv.reader(f)
    for row in reader:
        class_lookup[row[0]] = row[1]


# Make image label->class converter
label_lookup = {}
with open(label_file) as f:
    reader = csv.reader(f)
    for row in reader:
        label_lookup[row[0]] = row[2]

 
# Get list of files
files = glob.glob(base_dir+'*')

# Create the directories
class_pattern = re.compile(r'/m/(.*)')
for class_name in class_lookup.keys():
    class_name = class_pattern.search(class_name).groups(1)[0]
    print(class_name)
    if not os.path.exists(base_dir+'images/'+class_name):
        os.mkdir(base_dir+'images/'+class_name)

# Move all the files
file_pattern = re.compile(r'/([a-zA-Z0-9]+).jpg')
for path in files:
    id_match = file_pattern.search(path)

    try:
        id_num = id_match.groups(1)[0]

        class_name = label_lookup[id_num]
        class_name = class_pattern.search(class_name).groups(1)[0]
        os.rename(path,base_dir+'images/'+class_name+'/'+id_num+'.jpg')
    except AttributeError:
        pass
