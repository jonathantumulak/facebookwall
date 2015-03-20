from django.contrib import admin
from wall.models import Status, Likes

# Register your models here.


class LikeInline(admin.TabularInline):
    model = Likes


class StatusAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['message', 'author']}),
        ("Date Published", {'fields': ['pub_date']}),
        ("Replies", {'fields': ['in_reply_to']})
    ]

    list_display = ('message', 'author', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['author']

    inlines = [LikeInline]

admin.site.register(Status, StatusAdmin)
