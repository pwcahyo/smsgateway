from django.db import models
from datetime import date

class Parent(models.Model):
	family_as = models.CharField(max_length=30)

	def __str__(self):
		return self.family_as

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "parent"

class SchoolType(models.Model):
	name = models.CharField(max_length=10)

	def __str__(self):
		return self.name

class School(models.Model):
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=25)
	address = models.CharField(max_length=40)
	school_type = models.ForeignKey(SchoolType, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "school"

class Major(models.Model):
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "major"

class NextMajor(models.Model):
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "next_major"

class Job(models.Model):
	name = models.CharField(max_length=40)

	def __str__(self):
		return self.name

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "job"

class Graduate(models.Model):
	name = models.IntegerField()

	def __str__(self):
		return str(self.name)

class Person(models.Model):
	#Create Table Person
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=25)
	address = models.CharField(max_length=40)
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	major = models.ForeignKey(Major, on_delete=models.CASCADE)
	next_major = models.ForeignKey(NextMajor, on_delete=models.CASCADE)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	graduate = models.ForeignKey(Graduate, on_delete=models.CASCADE)
	parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
	reg_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		#naming data in django admin
		return ("{0} / {1}".format(self.phone, self.name))

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "person"

class MessageStatus(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "message_status"

class Inbox(models.Model):
	#column definition with data type 
	phone = models.CharField(max_length=25)
	text = models.TextField(max_length=1000, blank=True)
	time = models.DateTimeField(auto_now_add=True)
	status = models.ForeignKey(MessageStatus, on_delete=models.CASCADE)

	def __str__(self):
		return self.phone

	# class Meta:
	# 	#rename table without app label
	# 	db_table = "inbox"

class Outbox(models.Model):
	#column definition with data type 
	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
	text = models.TextField(max_length=1000, blank=True)
	time = models.DateTimeField(auto_now_add=True)
	status = models.ForeignKey(MessageStatus, on_delete=models.CASCADE)
	school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
	major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)
	graduate = models.ForeignKey(Graduate, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.person)