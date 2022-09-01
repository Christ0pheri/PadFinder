import requests, re, time, urllib.parse, phonenumbers

import settings

def FindPads(filepath = "", baseurl = "", padnames = [], phone_numbers = [], urlextention = "", regex = "", verbose = False):
	ParseChats(filepath, baseurl = baseurl, padnames = padnames, urlextention = urlextention, regex = regex, verbose = verbose)
	for name in padnames:
		if verbose:
			print("Pad", name, "durchsuchen")
		text = OpenPads(baseurl = baseurl, padname = name, urlextention = urlextention, verbose = verbose)
		ParseText(text, regex = regex, baseurl = baseurl, padnames = padnames, verbose = verbose)
		ParsePhoneNumbers(text, regex = "\+?\d{2,5}\s?(?:\(\d\))?\s?\d{3,4}\s?\d+", phone_numbers = phone_numbers, padname = name, verbose = verbose)

def OpenPads(baseurl = "", padname = "", urlextention = "", verbose = False, sleep = 30):
	url = baseurl + padname + urlextention
	result = requests.get(url)
	text = result.text
	if text == "Too many requests, please try again later.": #result doesn't raise an exeption
		if verbose:
			print("Too many requests, trying again in {0} seconds.".format(sleep))
		time.sleep(sleep)
		return OpenPads(baseurl = baseurl, padname = padname, urlextention = urlextention, verbose = verbose)
	return text

def ParseText(text, regex = "", baseurl= "", padnames = [], verbose = False):
	urls = re.findall(regex, text)
	for index, url in enumerate(urls):
		start = len(baseurl)
		padname = url[start:]
		padname = urllib.parse.unquote(padname) #%20 to Spaces etc.

		if padname not in padnames:
			if verbose:
				print(padname, "zu Pads hinzufügen")
			padnames.append(padname)

def ParsePhoneNumbers(text, regex = "", phone_numbers = [], padname = "", verbose = False):
	matches = phonenumbers.PhoneNumberMatcher(text, "IN")
	for match in matches:
		number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
		if number not in phone_numbers:
			phone_numbers.append((number, padname))
		if verbose:
			print(number, "in", padname, "gefunden")
			#time.sleep(5)

def ParseChats(filepath, baseurl = "", padnames = [], urlextention = "", regex = "", verbose = False):
	with open(filepath) as f:
		content = f.read()
	ParseText(content, regex = regex, baseurl= baseurl, padnames = padnames, verbose = False)

def ExpPads(filepath, baseurl = "", padnames = [], verbose = False):
	padnames.sort()
	with open(filepath, "w") as f:
		for padname in padnames:
			url = baseurl + padname
			f.write(url + "\n")
def ExpNumbers(filepath, baseurl = "", phone_numbers = [], verbose = False):
	phone_numbers.sort()
	with open(filepath, "w") as f:
		for phonenumber in phone_numbers:
			number = phonenumber[0]
			padname = phonenumber[1]
			url = baseurl + padname
			f.write("{0} in {1} gefunden\n".format(number, url))

if __name__ == "__main__":
	import sys

	verbose = False

	if len(sys.argv) > 1:
		for index, arg in enumerate(sys.argv[1:], 1):
			if arg == "-v":
				verbose = True

	padnames = settings.padnames
	phone_numbers = []

	FindPads(filepath = settings.filepath, baseurl = settings.baseurl, padnames = padnames, phone_numbers = phone_numbers, urlextention = settings.urlextention, regex = settings.regex, verbose = verbose)
	#filepath = settings.filepath
	ExpPads(settings.filepath_export + "pads.txt", baseurl = settings.baseurl, padnames = padnames, verbose = verbose)

	ExpNumbers(settings.filepath_export + "numbers.txt", baseurl = settings.baseurl, phone_numbers = phone_numbers, verbose = verbose)

	if verbose:
		print(len(padnames), " Pads gefunden")
		padnames.sort()
		print(padnames)
		phone_numbers.sort()
		print(phone_numbers)