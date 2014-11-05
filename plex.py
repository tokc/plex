import time
from datetime import datetime
import urllib # this library has tools for fetching stuff from the web
from bs4 import BeautifulSoup # this library has tools for parsing html

import candle

v = False

def getPLEX():
	print "Fetching PLEX prices..."
	try:
		timerightnow = str(datetime.utcnow())
		# this is the url
		url = "http://api.eve-central.com/api/quicklook?typeid=29668&sethours=1"
		page = urllib.urlopen(url) # open up the webpage
		print page.getcode()
		
		quicklook = page.read()
		
		soup = BeautifulSoup(quicklook) # read the contents of the webpage
	
	except: # report that something bad happened
		print("! Something went wrong while reading the API.")
		pass
	finally:
		try:
			page.close() # close the .urlopen() from before
		except: # if there's nothing to close
			print("! Something went wrong while trying to close the page.")
			pass # do nothing
	
	xmlfile = "xml/quicklook.xml"
	xmlopen = open(xmlfile, "w")
	
	if v: print "writing to quicklook.xml"
	xmlopen.write(quicklook)
	
	minsell = ""
	minsell = []
	selltest = ""
	selltest = []
	
	maxbuy = ""
	maxbuy = []
	
	jitabuy = ""
	jitabuy = []
	
	aridia = ""
	aridia = []
	
	aridiatoggle = 1
	
	if v: print "sorting sells..."
	try:
		for price in soup.sell_orders.find_all('price'):
			minsell.append(float(price.string))
			selltest.append([float(price.string), price.parent.station_name.string])
		minsell.sort()
		selltest.sort()
	except:
		print "! Something went wrong with sorting."
		pass
	
	if v: print "sorting buys..."
	try:
		for order in soup.buy_orders.find_all('order'):
			if order.station.string == "60003760":
				jitabuy.append(float(order.price.string))
		jitabuy.sort()
		jitabuy.reverse()
		
		for price in soup.buy_orders.find_all('price'):
			maxbuy.append(float(price.string))
		maxbuy.sort()
		maxbuy.reverse()
		
	except:
		print "! Something went wrong with sorting buys."
		pass
	
	if v: print "writing to files..."
	try:
		file2 = open("data/sell.txt", "a")
		file2.write(timerightnow.partition('.')[0] + " sell " + str(minsell[0])
			+ "\n")
		if (minsell[0] < 601000000):
			file2.write(timerightnow.partition('.')[0] + " sell "
				+ str(minsell[1]) + "\n")
		file2.close()
		
		file = open("data/buy.txt", "a")
		file.write(timerightnow.partition('.')[0] + " buy " + str(maxbuy[0])
			+ "\n")
		
		file.close()
		
		file = open("data/jitabuy.txt", "a")
		file.write(timerightnow.partition('.')[0] + " jitabuy "
			+ str(jitabuy[0]) + "\n")
		file.close()
		
		file4 = open("data/jitabuy.txt", "r")
		
		file3 = open("multichartPLEX1.txt", "w")
		
		file3.write(file4.read())
		
		file3.close()
		file4.close()
		
	except:
		print "! Something went wrong with files."
		pass
		
	try:
		if v: print "Jita buy:  ", float( int((jitabuy[0] / 10000)) / 100)
		else: print "Jita buy:  ", int((jitabuy[0] / 10000)) / 100
		if v: print ("7% spr: "
			+ str( float( int((jitabuy[0] * 0.93) / 10000) / 100) )
			+ "  5% spr: "
			+ str( float( int((jitabuy[0] * 0.95) / 10000) / 100) )
			+ "  3% spr: "
			+ str( float( int((jitabuy[0] * 0.97) / 10000) / 100) ))
		print ("[" + timerightnow.partition('.')[0] + "] Lowest sell is "
			+ "(" + str(selltest[0][0]) + str(selltest[0][1]) + " + 2%: " + str(selltest[0][0] * 1.02))
		if v: print ("[" + timerightnow.partition('.')[0] + "] Highest buy is "
			+ str(maxbuy[0]))
		if v: print ("[" + timerightnow.partition('.')[0] + "] Jita buy is "
			+ str(jitabuy[0]))
		
		print selltest[0]
		
	except:
		print "! Something went wrong with... print?"
		pass

getPLEX()

while 1:
	if v: print "candlesticks..."
	
	try:
		candle.candlesticks()
	except:
		print "uh-oh..."
		pass
	
	getPLEX()
	print "sleeping..."
	time.sleep(300)
