from django.urls import path
from django.views.decorators.cache import cache_page

from journal.views import (
    IndexView,
    JournalCreateView,
    JournalDeleteView,
    JournalDetailView,
    JournalListView,
    JournalUpdateView,
)

from .apps import JournalConfig

app_name = JournalConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("journal_list/", JournalListView.as_view(), name="journal_list"),
    path("journal/create/", JournalCreateView.as_view(), name="entry_create"),
    path(
        "journal/<int:pk>/detail/",
        cache_page(60)(JournalDetailView.as_view()),
        name="entry_detail",
    ),
    path("journal/<int:pk>/update/", JournalUpdateView.as_view(), name="entry_update"),
    path("journal/<int:pk>/delete/", JournalDeleteView.as_view(), name="entry_delete"),
]
