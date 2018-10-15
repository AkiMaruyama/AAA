import csv
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(filename):
	file_list = []
	with open(os.path.join(BASE_DIR, filename), 'r') as f:
		reader = csv.reader(f)
		file_list = list(reader)
	return file_list
#print (read_file('data/Comparison Parameters - Sheet1.csv')[1][2])
# data = read_file('data/Comparison Parameters - Sheet1.csv')
# print (len(data))
