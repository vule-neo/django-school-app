from django.contrib import admin

from .models import *

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(FileUpload)
admin.site.register(Comments)
admin.site.register(Likes)
