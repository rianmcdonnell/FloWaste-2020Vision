import glob, imghdr, os, sys

mode = sys.argv[1]
path = './data_v6/'

# Some of the images were corrupt and need to be deleted
blacklist = open('blacklist.txt','w')
id_list = open('id_list.txt', 'w')
base_dir = f'{path}{mode}/'

# Iterate through each directory
dirs = glob.glob(base_dir+'*')
for i, item in enumerate(dirs):
    print(f'{i+1}/{len(dirs)}')

    # Iterate through each file
    files = glob.glob(item+'/*')
    for filename in files:
        # Delete and log any file that has a corrupted format
        extension = filename.split('.')[-1]

        if extension == 'jpg':
            extension = 'jpeg'

        if extension != imghdr.what(filename):
            os.remove(filename)
            blacklist.write(filename+'\n')
        else:
            id_list.write(filename+'\n')

blacklist.close()
