import csv
import multiprocessing
import requests
import shutil
import sys, os

path = './data_v6/'
mode = sys.argv[1]
if not os.path.exists(path+mode+'/'):
    os.mkdir(path+mode+'/')

#read in all the data
with open(path+mode+'-parsed-images.csv') as f:
	reader = csv.reader(f)
	image_data = list(reader)

#get a list of urls
#image id is field 0, url is field 2
image_data = [(i[0],i[2]) for i in image_data]

#field is (id,url)
def download_img(field):
    img_id,url = field
    file_type = url.split('.')[-1]

    res = requests.get(url,stream=True)
    
    with open(path+mode+'/'+img_id+'.'+file_type,'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw,f)

    del res

cpus = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cpus)
pool.map(download_img,image_data)
