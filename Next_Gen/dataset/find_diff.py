#Finds all classes which are both food and have segmentation data
import csv

with open('class-descriptions-boxable.csv') as f:
	reader = csv.reader(f)
	data = list(reader)

ideal_ids = [i[0] for i in data]
#print(ideal_ids)

with open('classes-segmentation.txt') as f:
	data2 = f.readlines()
	data2 = [i.strip() for i in data2]

present_ids = set(data2)

parsed_list = []

for i,item in enumerate(ideal_ids):
	if item in present_ids:
		print(data[i][1])
		parsed_list.append(data[i])

with open('classes-segmentable.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(parsed_list)
