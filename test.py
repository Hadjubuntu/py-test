#!/usr/bin/env python
# coding: utf-8


import time
from multiprocessing import Queue
from threading import Thread
import threading


shareStack = {}
lock = threading.Lock()

class Worker(Thread):
	def __init__(self, pWorkerIdx, pQueueOfWork, pLock):		
		Thread.__init__(self)
		self.workerIdx = pWorkerIdx
		self.queueOfWork = pQueueOfWork
		self.lock = pLock

		print("Worker woke-up #" + str(self.workerIdx))

	def quit(self):
		self.isActive = False

	def run(self):
		global shareStack
		
		print("Worker executed")
		self.isActive = True

		while self.isActive:
			workToDo = self.queueOfWork.get()
			print("Worker #" + str(self.workerIdx) + " has done work #" + str(workToDo))

			if workToDo == 'quit':
				self.quit()
			else:
				self.lock.acquire()
				shareStack[workToDo] = 'result ' + str(self.workerIdx)				
				print("Stack size: " + str(len(shareStack)))
				self.lock.release()

		print("Worker #" + str(self.workerIdx) + " has qutited on command")


class WorkerManager(Thread):	
	def __init__(self):
		Thread.__init__(self)
		print("Worker Manager initialized")
		self.queueOfWork = Queue()
		self.workers = []
		self.lock = threading.Lock()

	def startWorkers(self):
		for worker in self.workers:
			worker.start()

	def joinWorkers(self):
		for worker in self.workers:
			worker.join()
	

	def run(self):
		print("Worker Manager executed")
		nWorkers = 8
		nWorkToDo = 1000000
		global shareStack

		self.workers = [Worker(idx+1, self.queueOfWork, self.lock) for idx in range(0, nWorkers)]
		print("There is " + str(len(self.workers)) + " workers ready to work")

		self.startWorkers()

		for i in range(1, nWorkToDo):
			self.queueOfWork.put("Work todo : #"+str(i))

		while len(shareStack) < nWorkToDo:
			print("Still work todo : " + str(len(shareStack)))
			time.sleep(0.5)

		print("Quit workers")
		for i in range(1, 1000): # TODO FIXME !!! C'est moche, il vaut mieux faire: Tant que worker alive, then send quit command..
			self.queueOfWork.put("quit")

		print("Workers have quitted")

		self.joinWorkers()
		print("Join all workers")


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

print("------------------------------")

workerManager = WorkerManager()
workerManager.start()
workerManager.join()