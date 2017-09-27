from __future__ import print_function
import requests, re, sys

"""Israel Felhandler"""
"""IF12B"""
"""CIS4930 - Python"""
"""Summer 2017"""


url = "http://www.cs.fsu.edu/department/faculty/"
keywords = {"Name": "Name", "Office": "Office", 
"Telephone": "Telephone", "E-Mail": "E-Mail"}

def get_info():
	main_page = requests.get(url)

	#Get all links to teachers websites
	links = re.findall(r'<td style="text-align: center;"><a href="([^"]+)">', main_page.text)
	for link in links:
		teacher_page = requests.get(link)
		#Get_teacher_info and save it into a dictionary
		temp = dict(get_teacher_info(teacher_page))
		
		print ("Name: " + temp['Name'])
		print ("Office: " + temp['Office'])
		print ("Telephone: " + temp['Telephone'])
		print ("E-Mail: " + temp['E-Mail'])
		print("****************************************")

def get_teacher_info(teacher_page):
	results = []
	#Iterate through the keywords and get the desired info
	for keyword in keywords.values():
		data = get_info_by_keyword(teacher_page, keyword)
		if data:
			results.append((keyword, data))
	return results

def get_info_by_keyword(teacher_page, keyword):	
	if keyword == "Name":
		data = re.search(r'<h1 class="main_title">([^<]+)</h1>',
			teacher_page.text,re.S)
		if data:
			return data.group(1)
		#Panama City webpage
		else:
			data = re.search(r'<title>([^|]+)\|',
				teacher_page.text,re.S)
			if data:
				return data.group(1)
			else:
				return "N/A"
			
	elif keyword == "Office":
		data = re.search(keyword + r':</strong></td>\n<td>([^<]+)</td>',
			teacher_page.text, re.S)
		if data:
			return data.group(1)
		else:
			data = re.search(r'office-location.*?item">([^<]*)</div>',
				teacher_page.text, re.S)
			if data:
				return data.group(1)
			else:
				return "N/A"
	elif keyword == "Telephone":
		data = re.search(keyword + r':</strong></td>\n<td>([^<]+)</td>',
			teacher_page.text, re.S)
		if data:
			return data.group(1)
		else:
			data = re.search(r'Phone</div>.*?item">([^<]*)</div>',
				teacher_page.text, re.S)
			if data:
				return data.group(1)
			else:
				return "N/A"
	elif keyword == "E-Mail":
		data = re.search(keyword + r':</strong></td>\n<td>([^<]+)</',
			teacher_page.text, re.S)
		if data:
			return data.group(1)
		else:
			data = re.search(r'><a href="mailto:([^"]*)">', 
				teacher_page.text, re.S)
			if data:
				return data.group(1)
			else:
				return "N/A" 
	return None

if __name__ == "__main__":
	get_info()