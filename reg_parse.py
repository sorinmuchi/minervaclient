#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib
import sys
import codecs
from minerva_common import *

def quick_add_insert(text,crns):
	html = BeautifulSoup(text,'html.parser')
	forms = html.body.find_all('form')
	reg = forms[1]
	inputs = reg.find_all(['input','select'])
	request = []


	for input in inputs:
		
		if not input.has_attr('name'): 
			if input.has_attr('id'):
				print "This is an actual problem"
			else: 
				continue

		
		if input.has_attr('value'): #This should always fail for a select.
			val = input['value']
		else:
			val = ''

		if val == 'Class Search':  #We want to register and not search,
			continue

		if crns and input['name'] == 'CRN_IN' and val == '':  # Shove our CRN in the first blank field
			val = crns.pop(0)

		request.append((input['name'], val))
	
	
	return urllib.urlencode(request)

def quick_add_status(text):
	html = BeautifulSoup(text,'html.parser')
	errtable = html.body.find('table',{'summary':'This layout table is used to present Registration Errors.'})
	if errtable is not None:
			error = errtable.findAll('td',{'class': "dddefault"})[0].a.text
			if error.startswith("Open"):
				print "* Must enter the waitlist section."
				return MinervaError.reg_wait
			else:	
				print "\033[1m* Failed to register: \033[0m " + str(error)
				return MinervaError.reg_fail
	

	print "\033[1m* Registration probably suceeded.\033[0m"
	return MinervaError.reg_ok

def quick_add_wait(text):
	html = BeautifulSoup(text,'html.parser')
	forms = html.body.find_all('form')
	reg = forms[1]
	inputs = reg.find_all(['input','select'])
	request = []


	for input in inputs:
		
		if not input.has_attr('name'): 
			if input.has_attr('id'):
				print "This is an actual problem"
			else: 
				continue

		
		if input.has_attr('value'): #This should always fail for a select.
			val = input['value']
		else:
			val = ''


		if input.has_attr('id') and input['id'].startswith('waitaction'):
			val = 'LW'

		request.append((input['name'], val))
	
	return urllib.urlencode(request)
