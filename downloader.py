import urllib.request
import re
import sys
import os

def downloadComics(id):
	founddata = True
	start = 0
	downloaded = 0
	downloaddir = None
	finished = False
	while founddata and not finished:
		founddata = False
		url = "https://www.hs.fi/rest/laneitems/39221/moreItems?from="+str(start)+"&pageId="+id+"&even=true"
		page = urllib.request.urlopen(url)
		data = page.read().decode("utf8")
		list = data.split('<li class="list-item cartoon">')
		for item in list:
			urlsearch = re.search('data-srcset="//(.*) ', item)
			datesearch = re.search('datePublished" content="(.*)">', item)
			if not downloaddir:
				namesearch = re.search('<span class="title">(.*)</span>', data)
				if namesearch:
					downloaddir = namesearch.group(1)
					print("Found "+downloaddir)
				else:
					print("Something went wrong!")
					return
				if not (os.path.isdir("downloads")):
					os.mkdir("downloads")
				if not (os.path.isdir("downloads/"+downloaddir)):
					print("Creating download directory: "+downloaddir)
					os.mkdir("downloads/"+downloaddir)
				
			
			if urlsearch and datesearch:
				founddata = True
				url = "https://"+urlsearch.group(1)
				date = datesearch.group(1)
				filename = date+"-"+url.split("/")[-1]
				if os.path.exists("downloads/"+downloaddir+"/"+filename):
					print(filename+" already exists. Assuming the download is done.")
					finished = True
					break
				print("Downloading "+downloaddir+" "+date+": "+url)
				urllib.request.urlretrieve(url, "downloads/"+downloaddir+"/"+filename)
				downloaded += 1
		start += 10
	print("Downloaded "+str(downloaded)+" "+downloaddir+" comic strips.")
	
def getIds():
	idList = []
	url = "https://www.hs.fi/sarjakuvat"
	page = urllib.request.urlopen(url)
	data = page.read().decode("utf8")
	list = data.split('<li class="list-item cartoon">')
	list = list[1:]
	for item in list:
		urlsearch = re.search('<a href="/(.*)/', item)
		if urlsearch:
			url = "https://www.hs.fi/"+(urlsearch.group(1))+"/"
			#print(url)
			page = urllib.request.urlopen(url)
			data = page.read().decode("utf8")
			idsearch = re.search('data-page-id="(.*)" ', data)
			data = data.split('<li class="list-item cartoon">')[1]
			namesearch = re.search('<span class="title">(.*)</span>', data)
			id = idsearch.group(1)
			name = namesearch.group(1)
			print(name+": "+id)
			idList.append(id)
	return idList
			
if (len(sys.argv) >= 2):
	if (str(sys.argv[1]) == "all"):
		print("Preparing to download using all valid IDs:")
		list = getIds()
		for item in list:
			downloadComics(item)
	else:
		id = str(sys.argv[1])
		downloadComics(id)
else:
	print("Usage:\ndownloader.py <ID> - Download using a known ID\ndownloader.py all - Download using all valid IDs")
	print("\nValid IDs:")
	getIds()