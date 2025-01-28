from rest_framework.routers import SimpleRouter

from .apps import JournalConfig
from .views import DiaryEntryViewSet

app_name = JournalConfig.name

router = SimpleRouter()
router.register(r"", DiaryEntryViewSet, basename="entry")

urlpatterns = []
urlpatterns += router.urls
