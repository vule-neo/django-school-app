from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UploadFileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .decorators import allowed_users, teacher_student
from django.contrib.auth.decorators import login_required
import datetime
from online_users.models import OnlineUserActivity
from django.core.files.storage import FileSystemStorage


teacher_access_codes = ["2MlJbiUw", "yhQT1yBl", "vGeYgwym","CQacGkGP",
						"Jfl2YAm5", "9JEkpcaK", "r3d9ouZr", "HNiAMsAm",
						"KqSz9vTa", "S2QQks5L", "jGdg25Qc", "bDr3OuGY",
						"B08GIKyX", "VJDiq1Yu", "HzE3psVe", "pIZUcaPo",
						"ugko8fG5", "2UiAgjSY", "ZkGueg3c", "b5FoSO6V", ]


def home(request):
	user_activity_objects = OnlineUserActivity.get_user_activities()
	number_of_active_users = user_activity_objects.count()

	users = User.objects.all()
	num_users = User.objects.all().count()
	all_students = []
	all_teachers = []

	for i in users:
		if i.groups.all()[0].name == "Students":
			all_students.append(i)
		elif i.groups.all()[0].name == "Teachers":
			all_teachers.append(i)
		else:
			pass

	ofline_students = len(all_students) - number_of_active_users

	context = {
		"number_of_active_users": number_of_active_users,
		"ofline_students": ofline_students,
		"all_students": len(all_students),
		"all_teachers": len(all_teachers),
	}
	return render(request, "school_template/index.html", context)

@login_required(login_url="school:login_page")
def about(request):
	return render(request, "school_template/about.html")

@login_required(login_url="school:login_page")
def subjects(request):
	subjects = Subject.objects.all()
	students = Student.objects.all()
	context = {"subjects": subjects, "students": students}
	return render(request, "school_template/cource.html", context)


@login_required
@allowed_users(["Students", "Teachers"])
def subject_detail(request, id):
	subject = Subject.objects.get(id=id)
	files = FileUpload.objects.filter(subject_upl=subject).order_by('-upload_date')
	comments = Comments.objects.all().order_by('-post_date')
	
	user = request.user

	if user.groups.all()[0].name == "Teachers":
		context = {"subject":subject, "files":files, "comments":comments}
		all_files = FileUpload.objects.all()

		if request.method == "POST":
			if request.POST.get("comment"):
				comment_text = request.POST.get("comment")
				comment_instance = Comments(comment=comment_text, author=request.user, for_subject=subject, post_date=datetime.datetime.now())
				if comment_instance is not None:
					comment_instance.save()

			if request.FILES:
				textarea_input = request.POST.get("uputstva", False)
				fajl = request.FILES.get("fajl", False)
				
				file = FileUpload(text=textarea_input, file=fajl, uploader=user, subject_upl=subject)
				if file not in all_files:
					file.save()
					return redirect("school:subject-detail", id=id)

		return render(request, "school_template/course-details-prof.html", context)


	elif user.groups.all()[0].name == "Students":
		if request.method == "POST":
			if request.POST.get("comment"):
				comment_text = request.POST.get("comment")
				comment_instance = Comments(comment=comment_text, author=request.user, for_subject=subject, post_date=datetime.datetime.now())
				if comment_instance is not None:
					comment_instance.save()

		context = {"subject":subject, "files":files, "comments":comments}
		return render(request, "school_template/course-details-student.html", context)

def delete_file(request, id):
	file = FileUpload.objects.get(id=id)
	file.delete()
	return redirect("school:subject-detail", id=file.subject_upl.id)

def delete_comment(request, id):
	comment = Comments.objects.get(id=id)
	comment.delete()
	return redirect("school:subject-detail", id=comment.for_subject.id)


def login_page(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("pass")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect("/")
		else:
			return redirect("school:login_page")
	return render(request, "school_template/login.html")


def registration_page(request):
	form = CreateUserForm()

	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password1 = request.POST.get("pass1")
		password2 = request.POST.get("pass2")
		user_data = {'username': username, "email":email, "password1":password1, "password2":password2}
		form = CreateUserForm(user_data)
		if form.is_valid():
			form.save()
			user = authenticate(request, username=username, password=password1)
			if user is not None:
				login(request, user)
				return redirect("school:teacher_or_student")
		else:
			return redirect("school:registration_page")

	context = {"form":form }
	return render(request, "school_template/register.html", context)

@login_required(login_url="school:login_page")
def logout_user(request):
	logout(request)
	return redirect("school:login_page")

@login_required(login_url="school:login_page")
@teacher_student(["Students", "Teachers"])
def teacher_or_student(request):
	return render(request, "school_template/teacher_or_student.html")

@teacher_student(["Students", "Teachers"])
def student_account(request):
	student_group = Group.objects.get(name="Students")
	user = request.user
	user.groups.add(student_group)
	return redirect("/")

@teacher_student(["Students", "Teachers"])
def teacher_account(request):
	teachers_group = Group.objects.get(name="Teachers")
	user = request.user
	if request.method == "POST":
		code = request.POST.get("code")
		if code in teacher_access_codes:
			user.groups.add(teachers_group)
			teacher_access_codes.remove(code)
			return redirect("/")
		else:
			user.delete()
			return redirect("school:registration_page")

	return render(request, "school_template/teacher_account.html")


def likes(request, id):
	comment = Comments.objects.get(id=id)

	if not comment.comment_likes:
		like_instance = Likes(num_of_likes= 1, for_comment=comment, user_who_liked=request.user)
		like_instance.save()
		comment.comment_likes = like_instance
		comment.save()
	else:
		if comment.comment_likes.user_who_liked != request.user:
			like = Likes.objects.get(for_comment=comment)
			like.num_of_likes += 1
			like.user_who_liked = request.user
			like.save()
	return redirect("school:subject-detail", id=comment.for_subject.id)