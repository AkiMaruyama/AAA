from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from re import findall,search 
import os
from .forms import LinkForm
import csv
from django.contrib import messages
from findPattern import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# URL = ['http://awardviewer.fwo.gov.au/award/show/MA000054#TopOfPage',
		# 'http://awardviewer.fwo.gov.au/award/show/MA000118#TOPOFBODYPAGE',
		# 'http://awardviewer.fwo.gov.au/award/show/MA000018#TopOfPage']

# index view
def index(request):
    return render(request, 'index.html')

def compare(request):
	context = {}
	
	if request.method == 'POST':
		url = request.POST['link']
		oh = extract_ordinary_hours(url)
		dh = extract_max_daily_hours(url)
		mh = extract_max_weekly_hours(url)
		cl = extract_casual_loading(url) 
		pr = extract_public_rate(url)
		
		if (pr == "double"):
			pr_int = 2
		
		context = { 
		'Ordinary Hours':  oh[0] + "am-" + oh[1] + "pm",
		'Max Daily': dh[0] + " hours",
		'Max Week': mh[0] + " hours",
		# 'overtime': overtime,
		# 'sat_rate': sat_rate,
		# 'sun_rate': sun_rate,
		'Casual Loading': cl + "%",
		'Public Holiday': pr + " times",
		}

		compared_condition = {
	 	'ordinary_hours': ['6am-10pm',int(oh[1])+12-int(oh[1]) <= 16 ],
		'max_daily': ['8 hours', int(dh[0]) <= 8],
		'max_week': ['38 hours', int(mh[0]) <= 38],
		# 'overtime': '38 hours',
		# 'sat_rate': '1.5x',
		# 'sun_rate': '1.5%',
		'casual_loading': ['30%',int(cl) >= 30],
		'public_holiday': ['2x',pr_int >= 2]
		}
	
	return render(request, 'compare.html', {
		'data': context.items(),
		'compared': compared_condition.values()
	})

# Create a compare page
def conditions(request):
    return render(request, 'conditions.html')