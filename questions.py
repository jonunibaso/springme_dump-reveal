#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.dom import minidom 

import urllib.request
import urllib.parse
import urllib.error

import getopt
import re
import sys

import io
import gzip

import json

import time
import glob

from lxml import etree

from bs4 import BeautifulSoup



class Buscador():

	def __init__(self):
		self.total = 0
		self.urls = []
		self.header = {   
			'User-Agent': 'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
			'Accept-Language': 'en-us',
			'Accept-Encoding': 'gzip, deflate, compress;q=0.9',
			'Keep-Alive': '300',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			}


		self.id = ''
		self.q = ''
		self.a = ''
		self.ab = ''
		self.lastId = ''
		self.f = ''

	
	def busca(self,name,pos):
		
		self.f = ''


		finalurl = "http://beta-api.formspring.me/answered/list/%s.xml?before=%s" % (name,pos)

		print ("Url: %s" % finalurl)
		req = urllib.request.Request(finalurl, None, self.header)
		response = urllib.request.urlopen(req)

		if response.info().get('Content-Encoding') == 'gzip':

			buf = io.BytesIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			the_page = f.read()
		else:
			the_page = response.read()


		soup = BeautifulSoup(the_page)

		for p in soup.find_all('item'):
			print('------------------------------------------')

			for i in p.find_all('id'):
				self.id = i.string
				self.lastId = self.id
				print ("ID: %s" %self.id)
				self.f += "\n-\nID: %s" %self.id
			
				self.c1(self.id)

			for ab in p.find_all('asked_by'):
				for us in ab.find_all('username'):
					if us:
						sus = str(us)
						fus = sus.replace('<username>','')
						fus = fus.replace('</username>','')

						print ("Asked by: %s" % fus)
						self.f += "\nAsked by: %s" % fus


			for q in p.find_all('question'):
				self.q = q.string
				print('-')
				print (self.q)
				self.f += "\nQ: %s" % self.q


			for a in p.find_all('answer'):
				self.a = a.string
				print('-')
				print (self.a)
				self.f += "\nA: %s\n\n" % self.a

			print('------------------------------------------')



	def c1(self,pos):


		finalurl = "https://api.spring.me/responses/index/%s" % (pos)

		print ("Url: %s" % finalurl)
		req = urllib.request.Request(finalurl, None, self.header)
		response = urllib.request.urlopen(req)


		if response.info().get('Content-Encoding') == 'gzip':

			buf = io.BytesIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			the_page = f.read()
		else:
			the_page = response.read()


		soup = BeautifulSoup(the_page)
		ssoup = str(soup)
		
		if ssoup.find('socrates-id') >= 0:

			pos = ssoup.find('socrates-id')
			pos2 = ssoup.find('text')
			si = ssoup[pos:pos2]
			si = si.replace('socrates-id":"','')
			si = si.replace('","','')
			if "null" not in si: 
				print ("Socrates: %s" %si)
				self.f += "\nSocrates: %s" % si

				self.c2(si)


	def c2(self,pos):


		finalurl = "https://api.spring.me/responses/view/%s" % (pos)
		existe = True
		print ("Url: %s" % finalurl)
		req = urllib.request.Request(finalurl, None, self.header)
		try:
			response = urllib.request.urlopen(req)

		except urllib.error.HTTPError:
			existe = False
			pass
		if(existe):
			if response.info().get('Content-Encoding') == 'gzip':

				buf = io.BytesIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				the_page = f.read()
			else:
				the_page = response.read()


			soup = BeautifulSoup(the_page)
			ssoup = str(soup)
			
			if ssoup.find('asked_by') >= 0:

				pos = ssoup.find('asked_by')
				pos2 = ssoup.find('created')
				ab = ssoup[pos:pos2]
				ab = ab.replace('asked_by":"','')
				ab = ab.replace('","','')


				print ("Asked ANON BY: %s" %ab)
				self.f += "\nAsked ANON BY:: %s" % ab



def main():

	usuario = 'miguelagnes'

	busc = Buscador()

	last = ''
	firstI = ''

	for files in glob.glob("%s*.txt" % usuario):
		if firstI == "":
			firstI = files
	firstI = firstI.replace('%s-' % usuario,'')
	firstI = firstI.replace('.txt','')

	last = firstI
	
	tope = 100
	current = 0

	print ('Beggining %s search from qID: %s' % (usuario,last))
	
	for count in range(1, tope):

		busc.busca(usuario,last)
		#print (busc.f)
		
		path = '%s-%s.txt' % (usuario,busc.lastId)
		file_handler = open(path, 'w')
		file_handler.write(busc.f)
		file_handler.close()
		last = busc.lastId



if __name__ == "__main__":
	main()


