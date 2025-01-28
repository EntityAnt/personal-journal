from django.contrib import admin

from journal.models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "created_at",
        "owner",
    )
    list_filter = ("title",)
    search_fields = ("title", "content")
