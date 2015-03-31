from django.contrib import admin

from wall.models import Status, Like

# Register your models here.


class LikeInline(admin.TabularInline):
    model = Like


class StatusAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['message', 'user']}),
        ("Date Published", {'fields': ['pub_date']}),
        ("Replies", {'fields': ['in_reply_to']})
    ]

    list_display = ('message', 'user', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['user']

    inlines = [LikeInline]


admin.site.register(Status, StatusAdmin)
