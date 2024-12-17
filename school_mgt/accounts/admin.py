from django.contrib import admin
from .models import User,Student, LibraryHistory, FeesHistory,Librarian,OfficeStaff

admin.site.register(User)

admin.site.register(Student)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)
admin.site.register(Librarian)
admin.site.register(OfficeStaff)