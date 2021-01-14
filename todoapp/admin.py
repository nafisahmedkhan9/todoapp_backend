from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)

admin.site.register(Task)
admin.site.register(Bucket)