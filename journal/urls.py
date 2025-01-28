from rest_framework.routers import SimpleRouter
from .views import DiaryEntryViewSet
from .apps import JournalConfig

app_name = JournalConfig.name

router = SimpleRouter()
router.register(r"", DiaryEntryViewSet, basename="entry")

urlpatterns = []
urlpatterns += router.urls
