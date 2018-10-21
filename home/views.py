from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import subprocess
from threading import Thread
from Scripts.main import start_downoading
import threading, traceback
from multiprocessing import Process
from .models import *
from django.shortcuts import get_object_or_404
import signal
import psutil, time
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
# Create your views here.

# torrent_download = threading.Thread(target=start_downoading)
def Home(request):
	import os
	# output = script_function() 
	# return HttpResponse(output)
	if request.method == 'GET':
		obj=get_object_or_404(TorrentDownload, id=1)
		obj.percentage='0'
		obj.peers='0'
		print obj
		obj.save()
		return render(request,'home/home.html')
	elif request.method == 'POST':
		# print "POST Successfull"
		# torrent_download = threading.Thread(target=start_downoading)
	 	# torrent_download.daemon = True
	 	# torrent_download.start()

	 	folder = 'Scripts/' #request.path.replace("/", "_")
	 	uploaded_filename = request.FILES['file'].name
	 	BASE_PATH = '/home/bhavi/py_torrent_client/BittorentGui/'
	 	full_filename = os.path.join(BASE_PATH, folder, uploaded_filename)
	 	fout = open(full_filename, 'wb+')
	 	file_content = ContentFile( request.FILES['file'].read() )
	 	# print "File name", uploaded_filename
	 	try:
	 		for chunk in file_content.chunks():
	 			fout.write(chunk)
	 		fout.close()
	 		# html = "<html><body>SAVED</body></html>"
	 		# return HttpResponse(html)
	 	except:
	 		html = "<html><body>FILE NOT SAVED</body></html>"
	 		return HttpResponse(html)

	 	global torrent_download
		torrent_download = Process(target=start_downoading,  kwargs={"file_name":uploaded_filename}) 	
	 	torrent_download.daemon = True
	 	torrent_download.start()
	 	return render(request,'home/downloading.html')
	 	# output = script_function() 
		return HttpResponse("Downloading")
	# return HttpResponse("Hi")

def Downloading(request):
	if request.method == 'POST':
		print "Stop Thread"
		torrent_download.terminate()
		return HttpResponseRedirect(reverse('home:home'))

def script_function():
	# print subprocess
	return subprocess.call(['python', 'Scripts/main.py'])
  # return subprocess.call(['subprocess.py'])

  # return subprocess.check_call(['/Scripts/main.py'])

def DownloadPercentage(request):
	# print "GET"
	if request.method == 'GET':
		obj = TorrentDownload.objects.filter(id=1)
		# print "in view",obj
		if(obj.count>0):
			return render(request, 'home/percentage.html',{"object":obj})
		else:
			return

def Pause(request):
	print "pause"
	if request.method == 'POST':
		psProcess = psutil.Process(pid=torrent_download.pid)
		psProcess.suspend()
		time.sleep(1000000);
		print "paused"
		return render(request,'home/downloading.html')


def Play(request):
	print "play"
	if request.method == 'POST':
		psProcess = psutil.Process(pid=torrent_download.pid)
		psProcess.resume()
		print "resumed"
		return render(request,'home/downloading.html')

def MagnetLink(request):
	if request.method == 'POST':
		magnet=request.POST.get('magnet')
		# print "Starting Convesion for magnet", magnet
		command = "python3 Scripts/manage.py '"+magnet+"'"
		# print "command is ",command
		# subprocess.call("ls")
		s=subprocess.call(['python', 'Scripts/magnet.py', str(magnet)], shell=False)
		f=open("Scripts/magnet-name.txt","r")
		name=f.readline()
		print "name=",name
		global torrent_download
		torrent_download = Process(target=start_downoading,  kwargs={"file_name":name}) 	
	 	torrent_download.daemon = True
	 	torrent_download.start()
	 	return render(request,'home/downloading.html')

		# print "sss",s
		return HttpResponse("done")
		# subprocess.call('python3 magnet.py "hi"')
