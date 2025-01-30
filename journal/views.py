from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

import journal
from .models import DiaryEntry
from .paginations import CustomPagination
from .serializers import DiaryEntrySerializer


class IndexView(TemplateView):
    template_name = "journal/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"

        return context_data


class JournalListView(ListView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DiaryEntry.objects.all()
        return DiaryEntry.objects.filter(owner=self.request.user.id)


class JournalDetailView(DetailView):
    model = DiaryEntry


class JournalCreateView(CreateView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    fields = ("title", "content", "owner")
    success_url = reverse_lazy("journal:journal_list")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JournalUpdateView(UpdateView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    fields = ("title", "content", "owner")
    success_url = reverse_lazy("journal:journal_list")


class JournalDeleteView(DeleteView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    success_url = reverse_lazy("journal:journal_list")


class DiaryEntryViewSet(viewsets.ModelViewSet):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    # def get_queryset(self):
    #     return DiaryEntry.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DiaryEntry.objects.all()
        return DiaryEntry.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
