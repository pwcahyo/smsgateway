from django.db import models
from datetime import date

class SentBoxCoba(models.Model):
	#column definition with data type 
	number = models.CharField(max_length=25)
	message = models.TextField(max_length=1000, blank=True)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now=True)

	class Meta:
		#rename table without app label
		db_table = "SentBoxCoba"



