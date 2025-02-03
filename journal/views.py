from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

import journal
from .forms import DiaryEntryForm
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
    permission_classes = [IsAuthenticated]


class JournalCreateView(CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    permission_classes = [IsAuthenticated]
    success_url = reverse_lazy("journal:journal_list")


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class JournalUpdateView(UpdateView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    form_class = DiaryEntryForm
    permission_classes = [IsAuthenticated]
    success_url = reverse_lazy("journal:journal_list")


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class JournalDeleteView(DeleteView):
    model = DiaryEntry
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]
    success_url = reverse_lazy("journal:journal_list")


