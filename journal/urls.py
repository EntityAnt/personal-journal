from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter

from .apps import JournalConfig
from journal.views import DiaryEntryViewSet, IndexView, JournalListView, JournalCreateView, JournalUpdateView, \
    JournalDetailView, JournalDeleteView

app_name = JournalConfig.name

router = SimpleRouter()
router.register(r"", DiaryEntryViewSet, basename="entry")

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # path("journal/", DiaryEntryViewSet.as_view({'get': 'list'}, permission_classes=(AllowAny,)), name="journal"),
    path("journal_list/", JournalListView.as_view(), name="journal_list"),
    path("journal/create/", JournalCreateView.as_view(), name="entry_create"),
    path("journal/<int:pk>/detail/", JournalDetailView.as_view(), name="entry_detail"),
    path("journal/<int:pk>/update/", JournalUpdateView.as_view(), name="entry_update"),
    path("journal/<int:pk>/delete/", JournalDeleteView.as_view(), name="entry_delete"),

]
urlpatterns += router.urls
