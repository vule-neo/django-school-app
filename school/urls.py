from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "school"

urlpatterns = [
	path("", home, name="home"),
	path("about/", about, name="about"),
	path("subjects/", subjects, name="subjects"),

	path("login/", login_page, name="login_page"),
	path("logout/", logout_user, name="logout_user"),
	path("register/", registration_page, name="registration_page"),

	path("teacher-or-student/", teacher_or_student, name="teacher_or_student"),
	path("subject-detail/<int:id>/", subject_detail, name="subject-detail"),
	path("student-account/", student_account, name="student-account"),

	path("teacher-account/", teacher_account, name="teacher-account"),
	path("delete_file/<int:id>/", delete_file, name="delete_file"),
	path("delete_comment/<int:id>/", delete_comment, name="delete_comment"),

	path("likes/<int:id>/", likes, name="likes"),
	

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

