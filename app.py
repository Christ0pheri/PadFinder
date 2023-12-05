import requests, re, time, urllib.parse, phonenumbers
from email_validator import validate_email, EmailNotValidError

import settings

def FindPads(filepath = "", baseurl = "", padnames = [], phone_numbers = [], email_adresses = [], urlextention = "", regex = "", verbose = False):
	ParseChats(filepath, baseurl = baseurl, padnames = padnames, urlextention = urlextention, regex = regex, verbose = verbose)
	for index, name in enumerate(padnames):
		if verbose:
			print("Pad", name, "durchsuchen")
			print(index + 1, "von", len(padnames))
		text = OpenPads(baseurl = baseurl, padname = name, urlextention = urlextention, verbose = verbose)
		if text == None:
			continue
		ParseText(text, regex = regex, baseurl = baseurl, padnames = padnames, verbose = verbose)
		ParsePhoneNumbers(text, phone_numbers = phone_numbers, padname = name, verbose = verbose)
		ParseEmails(text, emails = email_adresses, padname = name, verbose = verbose)

def OpenPads(baseurl = "", padname = "", urlextention = "", verbose = False, sleep = 30):
	url = baseurl + padname + urlextention
	try:
		result = requests.get(url)
	except requests.exceptions.MissingSchema:
		print("Keine gültige URL")
		return None
	except requests.exceptions.InvalidURL:
		print("Keine gültige URL")
		return None
	time.sleep(5)
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

def ParsePhoneNumbers(text, phone_numbers = [], padname = "", verbose = False):
	matches = phonenumbers.PhoneNumberMatcher(text, "IN")
	for match in matches:
		number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
		if number not in phone_numbers:
			phone_numbers.append((number, padname))
		if verbose:
			print(number, "in", padname, "gefunden")
			#time.sleep(5)

def ParseEmails(text, emails = [], padname = "", verbose = False):
	email_adresses = re.findall("[\w\-\.]+\@[\w\.\-]+\.\w{2,}", text)
	for email_adress in email_adresses:
		if verbose:
			print(email_adress)
		try:
			emailObject = validate_email(email_adress)
			email_adress = emailObject.email
			emails.append((email_adress, padname))
			if verbose:
				print(email_adress, "found in", padname)
		except EmailNotValidError as errorMsg:
			if verbose:
				print(email_adress, "gefunden, aber keine richtige E-Mail-Adresse")
				print(str(errorMsg))

def ParseChats(filepath, baseurl = "", padnames = [], urlextention = "", regex = "", verbose = False):
	try:
		with open(filepath) as f:
			content = f.read()
	except FileNotFoundError:
		print("Chat file not found")
		return
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

def ExpEMails(filepath, baseurl = "", email_adresses = [], verbose = False):
	email_adresses.sort()
	with open(filepath, "w") as f:
		for entry in email_adresses:
			email_adress = entry[0]
			padname = entry[1]
			url = baseurl + padname
			f.write("{0} in {1} gefunden\n".format(email_adress, url))

if __name__ == "__main__":
	import sys

	verbose = False

	if len(sys.argv) > 1:
		for index, arg in enumerate(sys.argv[1:], 1):
			if arg == "-v":
				verbose = True

	padnames = settings.padnames
	phone_numbers = []
	email_adresses = []

	FindPads(filepath = settings.filepath, baseurl = settings.baseurl, padnames = padnames, phone_numbers = phone_numbers, email_adresses = email_adresses, urlextention = settings.urlextention, regex = settings.regex, verbose = verbose)
	#filepath = settings.filepath
	ExpPads(settings.filepath_export + "pads.txt", baseurl = settings.baseurl, padnames = padnames, verbose = verbose)
	ExpNumbers(settings.filepath_export + "numbers.txt", baseurl = settings.baseurl, phone_numbers = phone_numbers, verbose = verbose)
	ExpEMails(settings.filepath_export + "EMailadresses.txt", baseurl = settings.baseurl, email_adresses = email_adresses, verbose = verbose)

	if verbose:
		print(len(padnames), " Pads gefunden")
		padnames.sort()
		print(padnames)
		phone_numbers.sort()
		print(phone_numbers)