from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from re import findall,search 
import os
from .forms import LinkForm
import csv
from django.contrib import messages

# extract information about ordinary_hours
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file = open(os.path.join(BASE_DIR, 'download.txt'), 'r')
text=file.read().replace('\n','').replace('-', ' ')

def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'txt'):

    # Import the function for opening online documents
    from urllib.request import urlopen

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    import re

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        TAG_RE = re.compile(r'<[^>]+>') 
        text_file.write(TAG_RE.sub('', web_page_contents))
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    TAG_RE = re.compile(r'<[^>]+>') 
    return TAG_RE.sub('', web_page_contents)

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
	elif link.lower() in 'asphalt industry award 2010': # this statement was added by Aki (n9534041)
		return file_list[5]
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

def link(request):
	context = {}
	if request.method == 'POST':
		link = request.POST['link']
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
		mini = content[10]
		mini_f = content[11]
		context = {'link': content,
					'ordinary_hours': ordinary_hours,
					'max_daily': max_daily,
					'max_week': max_week,
					'overtime': overtime,
					'sat_rate': sat_rate,
					'sun_rate': sun_rate,
					'casual_loading': casual_loading,
					'public_holiday': public_holiday,
					'mini': mini,
					'mini_f': mini_f,
					'name': name,
					'link': link
		}
	return render(request, 'link.html', context)

# Create a compare page
def compare(request):
    return render(request, 'compare.html')

# Create a compare page
def conditions(request):
    return render(request, 'conditions.html')