#/usr/bin/env python
#coding: utf-8

import os,sys,json,time
import websocket
import threading
import csv
from websocket import create_connection

class order(object):
	def __init__(self, redisOrderType, masterCount, slaverCount, memory, area, name, password):
		self.redisOrderType = redisOrderType
		self.masterCount = masterCount
		self.slaverCount = slaverCount
		self.memory = memory
		self.area = area
		self.name = name
		self.password = password
	def strify(self):
		res = {}
		res["type"] = self.redisOrderType
		res["masterCount"] = self.masterCount
		res["slaverCount"] = self.slaverCount
		res["memory"] = self.memory
		res["area"] = self.area
		res["name"] = self.name
		res["password"] = self.password
		return json.dumps(res, indent=4).encode("utf-8")

class args(object):
	def __init__(self, actionOrderType, order, user):
		self.actionOrderType = actionOrderType
		self.order = json.loads(order)
		self.user = user
	def strify(self):
		res = {}
		res["type"] = self.actionOrderType
		res["order"] = self.order
		res["user"] = self.user
		return json.dumps(res, indent=4).encode("utf-8")

class command(object):
	def __init__(self, commandName, args):
		self.commandName = commandName
		self.args = json.loads(args)
	def strify(self):
		res = {}
		res["commandName"] = self.commandName
		res["args"] = self.args
		return json.dumps(res, indent=4).encode("utf-8")

class websocketClient(threading.Thread):
	def __init__(self, address, message):
		self.address = address
		self.message = json.loads(message)
		self.ws = websocket.WebSocketApp(self.address,
			on_message = self.on_message,
			on_error = self.on_error,
			on_close = self.on_close)

	def on_message(self, ws, message):
		print message

	def on_error(self, ws, error):
		print error

	def on_close(self, ws):
		print "### closed ###"

	def run(self):
		print self.message
		self.ws.send(self.message)

class dataParse(object):
	def __init__(self, filepath):
		self.filepath = filepath
	def openfile(self):
		self.reader = csv.reader(open(self.filepath))
		return self.reader

def sendMessage():
	DataParse = dataParse("D:/XXXX.csv")
	reader = DataParse.openfile()
	for line in reader:
		print line

def main():
	# sendMessage()
	Order = order("C", 1, 0, "2gb", "XXXX", "RedisName", 0)
	res = Order.strify()
	Args = args("NEWREDIS", Order.strify(), "Jason")
	Command = command("redisOrder", Args.strify())
	#WebsocketCleint = websocketClient("ws://host:port/v1/websocket",Command.strify())
	# print Command.strify()
	try:
		ws = create_connection("ws://10.101.20.52:8091/v1/websocket")
		res = Command.strify()
		#ws = websocket.WebSocket()
		#ws.connect()
		print res
		while(1):
			ws.send(res)
			time.sleep(5)
		ws.close()
	except Exception,e:
		pass
		#ws.close()

if __name__ == "__main__":
	main()
