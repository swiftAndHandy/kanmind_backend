from django.contrib import admin

from board_app.models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner']
    list_display_links = ['id', 'title']

admin.site.register(Board, BoardAdmin)
