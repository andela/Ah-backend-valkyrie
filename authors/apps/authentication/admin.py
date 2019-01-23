from django.contrib import admin
from .models import User


class MyAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')

admin.site.register(User, MyAdmin)