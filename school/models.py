from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
	name = models.CharField(max_length=50)
	surename = models.CharField(max_length=50)
	subject_name = models.ForeignKey("Subject", on_delete=models.CASCADE, null=True, blank=True)
	forum_class = models.ManyToManyField("Class", blank=True)
	picture = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.name


class Subject(models.Model):
	title = models.CharField(max_length=100)
	teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None, null=True, blank=True)
	def __str__(self):
		return self.title

class Class(models.Model):
	class Meta:
		verbose_name_plural = "classes"

	class_name = models.CharField(max_length=10)
	def __str__(self):
		return self.class_name


class Student(models.Model):
	name = models.CharField(max_length=50)
	surename = models.CharField(max_length=50)
	student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return self.name


class FileUpload(models.Model):
	text = models.CharField(max_length=300)
	file = models.FileField()
	upload_date = models.DateTimeField(auto_now_add=True)
	uploader = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	subject_upl = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.text

class Comments(models.Model):
	comment = models.CharField(max_length=400)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post_date = models.DateTimeField(auto_now_add=True)
	for_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	comment_likes = models.OneToOneField("Likes", null=True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.comment

class Likes(models.Model):
	num_of_likes = models.IntegerField()
	for_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
	user_who_liked = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.for_comment.comment