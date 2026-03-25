from django.contrib import admin

from auth_app.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'fullname']
    list_display_links = ['id', 'email']

admin.site.register(UserProfile, UserProfileAdmin)