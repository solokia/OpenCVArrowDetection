import threading
import sys
import time
import queue
from imageAPI import *


class Main(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.image_thread = imageAPI()
		print("init started")

	def test(self,distance):
		self.start = time.time()
		if(distance):
			self.image_thread.setFrame()
			msg = self.image_thread.run(distance)
			print("Time taken so far : ",(time.time()-self.start))
        
			return msg 

	def initialize_threads(self):
		rt_image = threading.Thread(target = self.test,args=("",),name ="image_read_thread")
		rt_image.daemon = True
		rt_image.start()
		print("thread start")

	def close_all_sockets(self):
		self.image_thread.close_all_image_sockets()
		print("thread closed")

	def keep_main_alive(self):
		while True:
			time.sleep(1)

if __name__ == "__maintest__":
	test = Main()
	test.initialize_threads()
	test.keep_main_alive()
	test.close_all_sockets()
