from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from re import findall,search 
import os
from .forms import LinkForm
import csv
from django.contrib import messages
from .findPattern import *
from .read_file import read_file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# URL = ['http://awardviewer.fwo.gov.au/award/show/MA000054#TopOfPage',
		# 'http://awardviewer.fwo.gov.au/award/show/MA000118#TOPOFBODYPAGE',
		# 'http://awardviewer.fwo.gov.au/award/show/MA000018#TopOfPage']

# index view
def index(request):
    return render(request, 'index.html')

def get_paras(num):
	data = read_file('data/Comparison Parameters - Sheet1.csv')[1:]
	results = []
	for i in range(len(data[1:])):
		if i % 2 != 0:
			results.append(data[1:][i][num])
	return (data[0][num],results)

def get_eba(num):
	data = read_file('data/EBA Phrasing Register - Sheet1.csv')[1:]
	conditions = data[0][1:]
	eba = data[num][1:]
	results = {}
	for i, value in enumerate(eba):
		results[conditions[i]] = value
	return (data[num][0],results)

def compare_eba(eba, award):
	results = []
	for i, value in enumerate(eba):
		if i == 0:
			result = findall(r"(\d+):",value)
			result2 = findall(r"(\d+):",award[i])
			a = int(result[1]) + 12 - int(result[0])
			b = int(result2[1]) + 12 - int(result2[0])
			results.append(a <= b)
		if i == 1 or i == 2 or i == 3:
			result = findall(r"(\d+(?:\.\d+)?)",value)
			result2 = findall(r"(\d+(?:\.\d+)?)",award[i])
			a = float(result[0])
			b = float(result2[0])
			results.append(a <= b)
		if i == 4 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9:
			result = findall(r"(\d+(?:\.\d+)?)",value)
			result2 = findall(r"(\d+(?:\.\d+)?)",award[i])
			a = float(result[0])
			b = float(result2[0])
			results.append(a >= b)
	return results


def compare(request):
	context = {}
	if request.method == 'POST':
		# url = request.POST['link']
		# url = 'http://awardviewer.fwo.gov.au/award/show/MA000118#TOPOFBODYPAGE'
		# oh = extract_ordinary_hours(url)
		# dh = extract_max_daily_hours(url)
		# mh = extract_max_weekly_hours(url)
		# cl = extract_casual_loading(url) 
		# pr = extract_public_rate(url)
		# sat_rate = extract_satday_rate(url)
		# sun_rate = extract_sunday_rate(url)
		
		# context = { 
		# 'Ordinary Hours of Work (Between what times)':  oh[0] + "am-" + oh[1] + "pm",
		# 'Maximum Daily Working Hour': dh[0] + " hours",
		# 'Maximum Weekly Working Hours': mh[0] + " hours",
		# # 'overtime': overtime,
		# 'Saturday Rate': str(sat_rate) + 'x',
		# 'Sunday Rate': str(sun_rate) + 'x',
		# 'Casual Loading': cl + "%",
		# 'Public Holiday Rate': str(pr) + "x",
		# }

		# compared_condition = {
	 	# 'ordinary_hours': ['6am-10pm',int(oh[1])+12-int(oh[1]) <= 16 ],
		# 'max_daily': ['8 hours', int(dh[0]) <= 8],
		# 'max_week': ['38 hours', int(mh[0]) <= 38],
		# # 'overtime': '38 hours',
		# 'sat_rate': ['1.5x', sat_rate >= 1.5],
		# 'sun_rate': ['2x', sun_rate >= 2],
		# 'casual_loading': ['30%',int(cl) >= 30],
		# 'public_holiday': ['2x',pr >= 2]
		# }
		# scores = 0
		# for i in compared_condition.values():
		# 	if i[1]:
		# 		scores+=1

		if request.POST.get('my_checkbox', False):
			eba = 'custome eba'
			context = { 
				'Ordinary Hours of Work': request.POST['ordinary_start'] + "am - " + request.POST['ordinary_end'] + "pm",
				'Maximum Daily Working Hour': request.POST['Maximum'],
				'Minimum Daily Working Hours': request.POST['Minimum'],
				'Maximum Weekly Working Hours': request.POST['Maximum Weekly'],
				'Public Holiday Rate': request.POST['Public Holiday'],
				'Overtime Conditions': request.POST['Overtime'],
				'Casual Loading': request.POST['Casual'],
				'Saturday Rate': request.POST['Saturday'],
				'Sunday Rate': request.POST['Sunday'],
				'Minimum Break Between Shifts': request.POST['Minimum Break']
			}
		else:
			eba, context = get_eba(int(request.POST['eba_select']))
		
		award, para = get_paras(int(request.POST['select']))
		a = compare_eba(context.values(), para)
		params = []
		scores = 0
		for i, each in enumerate(para):
			params.append({
				'value': each,
				'compared': a[i]
			})
			if a[i]:
				scores+= 10
	return render(request, 'compare_result.html', {
		'eba': eba,
		'award': award,
		'data': context.items(),
		'para': params,
		'score': scores
	})
