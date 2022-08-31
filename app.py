import requests, re, time

import settings

def FindPads(baseurl = "", padnames = [], urlextention = "", regex = "", verbose = False, sleep = False):
	for name in padnames:
		if verbose:
			print("Pad", name, "durchsuchen")
		text = OpenPads(baseurl = baseurl, padname = name, urlextention = urlextention)
		ParseText(text, regex = regex, baseurl = baseurl, padnames = padnames, verbose = verbose)
		ParsePhoneNumbers(text, regex = "\+?\d{2,5}\s?(?:\(\d\))?\s?\d{3,4}\s?\d+", phonenumbers = [], verbose = verbose)
		if sleep:
			time.sleep(5)

def OpenPads(baseurl = "", padname = "", urlextention = ""):
	url = baseurl + padname + urlextention
	result = requests.get(url)
	text = result.text
	return text

def ParseText(text, regex = "", baseurl= "", padnames = [], verbose = False):
	urls = re.findall(regex, text)
	for index, url in enumerate(urls):
		start = len(baseurl)
		padname = url[start:]
		#print(index, padname)

		if padname not in padnames:
			if verbose:
				print(padname, "zu Pads hinzufügen")
			#print(index, padname)
			padnames.append(padname)

def ParsePhoneNumbers(text, regex = "", phonenumbers = [], verbose = False):
	numbers = re.findall(regex, text)
	for number in numbers:
		if verbose:
			print(number)
			time.sleep(10)

if __name__ == "__main__":
	import sys

	verbose = False
	sleep = False

	if len(sys.argv) > 1:
		for index, arg in enumerate(sys.argv[1:], 1):
			if arg == "-v":
				verbose = True
			elif arg == "-s":
				sleep = True
	padnames = settings.padnames

	FindPads(baseurl = settings.baseurl, padnames = padnames, urlextention = settings.urlextention, regex = settings.regex, verbose = verbose, sleep = sleep)

	if verbose:
		print(len(padnames), " Pads gefunden")
		padnames.sort()
		print(padnames)