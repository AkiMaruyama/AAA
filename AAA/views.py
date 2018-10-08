from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from re import findall,search 
import os
from .forms import LinkForm
import csv
from django.contrib import messages
from download import *

# extract information about ordinary_hours
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file = open(os.path.join(BASE_DIR, 'download.txt'), 'r')
text=file.read().replace('\n','').replace('-', ' ')


def read_file(link):
	file_list = []
	with open(os.path.join(BASE_DIR, 'EBA Phrasing Register - Sheet1.csv'), 'r') as f:
		reader = csv.reader(f)
		file_list = list(reader)
	if link.lower() in 'supabarn eba':
		return file_list[2]
	elif link.lower() in 'atco eba':
		return file_list[3]
	elif link.lower() in 'armenian eba':
		return file_list[4]
	else:
		return None

def extract_ordinary_hours(text):
	ordinary_hours= search(r"([\w|\s]*?o|Ordinary hours[^.]*(\d+(?:\.\d+)?(?:\s[ap]m)? and \d+(?:\.\d+)?(?:\s[ap]m)?))", text)
	#ordinary_hours= search(r"([^a-z|A-Z| ]*?[o|O]rdinary hours[^.]*am and [^.]*\.)", text)
	if ordinary_hours is None:
		return "Not Found"
	return ordinary_hours[0]

def extract_max_daily_hours(text):
	pattern= search(r"([^a-z|A-Z| ]*?The maximum length[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_max_weekly_hours(text):
	pattern= search(r"Weekly hours of work[^a-zA-Z]+([^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_overtime_condition(text):
	pattern = search(r"([^a-z|A-Z]*?outside the ordinary hours[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0].title()

def extract_saturday_rate(text):
	pattern = search(r"([^.]*?on a Saturday[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_sunday_rate(text):
	pattern = search(r"([^a-z|A-Z]*?on Sundays[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0].title()

def extract_casual_loading(text):
	pattern = search(r"([\w|\s]*?casual employee[^.]*paid[^.]*[0-9][^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_public_holiday(text):
	pattern = search(r"([\w|\s]*?work on[^.]*public holiday[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_mini_break(text):
	pattern = search(r"([\w|\s]*?hours off duty[^.]*\.)", text)
	if pattern is None:
		return "Not Found"
	return pattern[0]

def extract_name(text):
	name = search(r"([\w|\s]* Award)", text)
	return name[0]

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # output = extract_overtime_condition()
    # context = {'name': output}
    return render(request, 'index.html')

compared_condition = {
 	'ordinary_hours': '5am-7pm',
	'max_daily': '8 hours',
	'max_week': '4 hours',
	'overtime': '38 hours',
	'sat_rate': '1.5x',
	'sun_rate': '1.5%',
	'casual_loading': '30%',
	'public_holiday': '2x',
}
def compare(request):
	context = {}
	if request.method == 'POST':
		# link = request.POST['link']
		link = 'armenian'
		# content = download(link)
		# ordinary_hours = extract_ordinary_hours(content)
		# max_daily = extract_max_daily_hours(content)
		# max_week = extract_max_weekly_hours(content)
		# overtime = extract_overtime_condition(content)
		# sat_rate = extract_saturday_rate(content)
		# sun_rate = extract_sunday_rate(content)
		# casual_loading = extract_casual_loading(content)
		# public_holiday = extract_public_holiday(content)
		# mini = extract_mini_break(content)
		# name = extract_name(content)

		"""
		new line
		"""
		content = read_file(link)
		if content == None:
			#return render_to_response('index.html', {'message':"Please enter again!"})
			return render(request, 'index.html')
		for i, each in enumerate(content):
			if each == '':
				content[i] = "Not Found"
		
		name = content[0]
		ordinary_hours = content[2]
		max_daily = content[3]
		max_week = content[4]
		overtime = content[5]
		sat_rate = content[6]
		sun_rate = content[7]
		casual_loading =content[8]
		public_holiday = content[9]
		context = { 'ordinary_hours': ordinary_hours,
					'max_daily': max_daily,
					'max_week': max_week,
					'overtime': overtime,
					'sat_rate': sat_rate,
					'sun_rate': sun_rate,
					'casual_loading': casual_loading,
					'public_holiday': public_holiday,
		}
	return render(request, 'compare.html', {'data': context.items(), 'compared': compared_condition.values()})

# Create a compare page
def conditions(request):
    return render(request, 'conditions.html')