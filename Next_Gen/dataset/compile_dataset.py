import csv, sys

download_path = './data_v6/'
temp_path = './temp/'
mode = sys.argv[1]

#read in all the data
with open(temp_path+mode+'-images-boxable-with-rotation.csv') as f:
	reader = csv.reader(f)
	image_data = list(reader)

with open(temp_path+mode+'-annotations-human-imagelabels-boxable.csv') as f:
	reader = csv.reader(f)
	label_data = list(reader)

with open(temp_path+mode+'-annotations-object-segmentation.csv') as f:
	reader = csv.reader(f)
	seg_data = list(reader)

#Read in the list of classes
with open('./classes-segmentable.csv') as f:
	reader = csv.reader(f)
	class_list = list(reader)
	class_list = set([i[0] for i in class_list])

print('Read data')

#Filter by label, then by segmentable
label_new = [i for i in label_data if i[2] in class_list]
valid_ids = set([i[0] for i in label_new])
seg_new = [i for i in seg_data if i[1] in valid_ids]
valid_ids = set([i[1] for i in seg_new])
label_new = [i for i in label_new if i[0] in valid_ids]
image_new = [i for i in image_data if i[0] in valid_ids]

print('Parsed Data')

#Then parse 
with open(download_path+mode+'-parsed-labels.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(label_new)

with open(download_path+mode+'-parsed-segs.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(seg_new)

with open(download_path+mode+'-parsed-images.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(image_new)


print('Finished')
