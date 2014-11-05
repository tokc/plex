# Pseudo-trade data generator.
# Creates something that resembles trade data (volume, price) from market data
# (bid, quantity) by looking for disappearing orders (and ASSUMING they were
# completely filled) and changes in quantity (these were definitely filled).

import time
from datetime import datetime
from bs4 import BeautifulSoup # this library has tools for parsing html

global t
t = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
v = False

def sortBUY():
	# parse xml into a dict {order ID: (remaining volume, price)}
	buylist = ""
	buylist = {1 : (1, 1, "TIME")}
	
	if v: print "Reading file..."
	xml = open("xml/quicklook.xml")
	soup = BeautifulSoup(xml.read())
	xml.close()
	
	if v: print "Extracting prices..."
	soup2 = soup.buy_orders.find_all('order')
	for order in soup2:
		if order.station.text == "60003760":
			buylist[int(order["id"])] = ( (int(order.vol_remain.string)), 
				int(float(order.price.string)) )
	return buylist

class getOldData():
	'read data corresponding to the previous "tick" from data.csv'
	
	def __init__(self):
		if v: print "Reading data from data.csv..."
		self.data = open("candle/data.csv", "r")
		self.olddata = self.data.read()
		self.previous = self.olddata.split("\n")
		self.data.close()
		
		if v: print "Parsing order checklist from data.csv..."
		self.checklist = {1 : (1, 1, "TIME")}
		for i in self.previous:
			a = i.split("%")
			if i:
				self.checklist[int(a[0])] = (int(a[1]), float(a[2]))

def fillVerbosity(key, value, reason):
	print "Found trade! Order number %s has %s. --- %s" % (str(key),
		str(reason), str(value))

def findFills(check, feed):
	trades = ""
	if v: print "Comparing orders..."
	for key, value in check.iteritems():
		if key not in feed:
			fillVerbosity(key, value, "disappeared")
			trades += str(int(value[0])) + "%" + str(value[1]) + "%" + str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) \
				+ "\n"
		
		elif value[0] > feed[key][0]:
			fillVerbosity(key, value, "changed")
			trades += str(int(value[0] - feed[key][0])) + "%" \
				+ str(value[1])	+ "%" + str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + "\n"
	return trades

def candlesticks():
	t = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	if v: print "candle.py"
	print t
	
	d = getOldData()
	datafeed = sortBUY()
	
	storeTrades(d.checklist, datafeed)
	backup(d)
	putOut(datafeed)

def storeTrades(check, feed):
	if v: print "Writing trades to trades.csv..."
	tradefile = open("candle/trades.csv", "a")
	tradefile.write(findFills(check, feed))
	tradefile.close()

def backup(d):
	if v: print 'Backing up old "tick" to backup.csv...'
	backup = open("candle/backup.csv", "w")
	backup.write(d.olddata)
	backup.close()

def putOut(feed):
	if v: print 'Writing new "tick" to data.csv...'
	
	output = []
	
	for key, value in feed.iteritems():
		a = str(key) + "%" + str(value[0]) + "%" + str(value[1]) + "%"
		output.append(a)

	data = open("candle/data.csv", "w")
	data.write("\n".join(output))
	data.close()
