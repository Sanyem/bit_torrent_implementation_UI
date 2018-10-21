from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TorrentDownload(models.Model):
	percentage=models.CharField(null=True,max_length=3)
	peers=models.CharField(null=True,max_length=10000)
	
	def __str__(self):
		return self.percentage