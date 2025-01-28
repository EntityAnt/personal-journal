from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import DiaryEntry
from .paginations import CustomPagination
from .serializers import DiaryEntrySerializer


class DiaryEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return DiaryEntry.objects.all()
        return DiaryEntry.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
