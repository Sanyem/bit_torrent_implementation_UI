

# if __name__ == '__main__':

def start_downoading(file_name):
	import run
	import logging
	print "FILE NAME ",file_name
	logging.basicConfig(level=logging.INFO)
	run = run.Run(file_name)
	run.start()
