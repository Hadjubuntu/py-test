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

	def specificJob(self):
		print("not implemented")

	def quit(self):
		self.isActive = False

	def run(self):
		global shareStack
		
		print("Worker executed")
		self.isActive = True

		while self.isActive:
			workToDo = self.queueOfWork.get()
			print("Worker #" + str(self.workerIdx) + " has done work #" + str(workToDo))

			# Handle work command
			if workToDo == 'quit':
				self.quit()
			else:
				if workToDo in shareStack:
					print("Work already done")
				else:
					self.lock.acquire()
					shareStack[workToDo] = 'result ' + str(self.workerIdx)				
					print("Stack size: " + str(len(shareStack)))
					self.lock.release()

				self.specificJob()

		print("Worker #" + str(self.workerIdx) + " has qutited on command")


class WorkerManager(Thread):	
	def __init__(self):
		Thread.__init__(self)
		print("Worker Manager initialized")
		self.queueOfWork = Queue()
		self.workers = []
		self.lock = threading.Lock()
		self.nWorkers = 8

	# Woke-up all workers
	def startWorkers(self):
		for worker in self.workers:
			worker.start()

	# Wait that all workers finished theirs works
	def joinWorkers(self):
		for worker in self.workers:
			worker.join()
	
	# Tells whether a thread is alive in a list of threads
	def isWorkerAlive(self, pWorkers):
		for worker in pWorkers:
			if worker.isAlive():
				return True

		return False

	# Create generic workers
	def createWorkers(self):
		self.workers = [Worker(idx+1, self.queueOfWork, self.lock) for idx in range(0, self.nWorkers)]
		print("There is " + str(len(self.workers)) + " workers ready to work")

	# Execute the manager: woke-up the workers and dispatch the work to them
	def run(self):
		print("Worker Manager executed")
		nWorkToDo = 100
		global shareStack

		# Create all workers
		self.createWorkers()

		# Start all workers (ready to work)
		self.startWorkers()

		for i in range(0, nWorkToDo):
			self.queueOfWork.put("Work todo : #"+str(i))

		while len(shareStack) < nWorkToDo:
			print("Still work todo : " + str(len(shareStack)))
			time.sleep(0.5)

		print("Quit workers")
		while self.isWorkerAlive(self.workers):
			self.queueOfWork.put("quit")

		print("Workers have quitted")

		self.joinWorkers()
		print("Join all workers")
