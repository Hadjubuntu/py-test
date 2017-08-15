#!/usr/bin/env python
# coding: utf-8


from WorkerManager import Worker, WorkerManager

# Implementation of worker
class SpecificWorker(Worker):
	def  specificJob(self):
		print("Yeah hellowwww")

# Implementation of worker manager
class SpecificWorkerManager(WorkerManager):
	# Create generic workers
	def createWorkers(self):
		self.workers = [SpecificWorker(idx+1, self.queueOfWork, self.lock) for idx in range(0, self.nWorkers)]
		print("There is " + str(len(self.workers)) + " workers ready to work")



# Test with worker and worker manager with Implementation
# ---
workerManager = SpecificWorkerManager()
workerManager.start()
workerManager.join()

# Same test with generic class
workerManager = WorkerManager()
workerManager.start()
workerManager.join()