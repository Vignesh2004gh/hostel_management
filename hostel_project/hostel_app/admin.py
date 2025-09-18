from django.contrib import admin
from .models import Student, MessCut, IceCream, StudentIceCream
# Register your models here.

admin.site.register(Student)
admin.site.register(MessCut)
admin.site.register(IceCream)
admin.site.register(StudentIceCream)