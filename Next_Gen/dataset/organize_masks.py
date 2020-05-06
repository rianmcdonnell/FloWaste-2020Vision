import glob, os, zipfile, csv, re, sys

temp_path = './temp/'
ref_path = './data_v6/'
mode = sys.argv[1]
data_path = f'{ref_path}{mode}/masks/'
class_file = './classes-segmentable.csv'
label_file = f'{ref_path}{mode}-parsed-labels.csv'

if not os.path.exists(data_path):
    os.mkdir(data_path)

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

# Create the directories
class_pattern = re.compile(r'/m/(.*)')
for class_name in class_lookup.keys():
    class_name = class_pattern.search(class_name).groups(1)[0]
    print(class_name)
    if not os.path.exists(data_path+class_name):
        os.mkdir(data_path+class_name)

# Loop through each zipped file
zippers = glob.glob(temp_path+ '*.zip')
file_pattern = re.compile(r'/([a-zA-Z0-9]+).png')

for zipped in zippers:
    with zipfile.ZipFile(zipped, 'r') as zip_ref:
        zip_ref.extractall(data_path)

    images = glob.glob(data_path+'*.png')
    for image in images:
        id_match = file_pattern.search(image)

    try:
        id_num = id_match.groups(1)[0]

        class_name = label_lookup[id_num]
        class_name = class_pattern.search(class_name).groups(1)[0]
        os.rename(image,data_path+class_name+'/'+id_num+'.jpg')
    except AttributeError:
        os.remove(image)
            

