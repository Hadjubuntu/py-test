#!/usr/bin/env python
# coding: utf-8


import time
from multiprocessing import Queue
from threading import Thread
import threading


shareStack = {}
lock = threading.Lock()


class TestThread(Thread):
	def __init__(self, pQueue, pValue):
		Thread.__init__(self)
		self.queue = pQueue
		self.value = pValue

	def run(self):
		global shareStack
		
		with lock:
			shareStack[self.value] = self.value

		# if not self.queue.empty():
		# 	print("Key exists \"test\" => " + str(self.queue.get()['test']))
		# else:
		# 	print("Queue empty")

		# self.queue.put({'test' : self.value})

	def printQueue(self):
		print(str(shareStack))
		# if not self.queue.empty():
		# 	print("Value: " + str(self.queue.get()))
		# else:
		# 	print("Queue empty")


# First part of test
# ---
q = Queue()
t1 = TestThread(q, "Hello 1 here")
t2 = TestThread(q, "Second 2 value")

print("t1 start")
t1.start()
print("t2 start")
t2.start()

t1.join()
print("t1 joined")
t2.join()
print("t2 joined")



print("t1 print")
t1.printQueue()
print("t2 print")
t2.printQueue()