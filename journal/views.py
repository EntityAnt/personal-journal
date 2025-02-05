from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import DiaryEntryForm
from .models import DiaryEntry


class IndexView(TemplateView):
    template_name = "journal/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"

        return context_data


class JournalListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    login_url = "users:login"

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = DiaryEntry.objects.all()
        else:
            queryset = DiaryEntry.objects.filter(owner=self.request.user)

        # Поиск по заголовку и контенту
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        return queryset


class JournalDetailView(LoginRequiredMixin, DetailView):
    model = DiaryEntry
    login_url = "users:login"


class JournalCreateView(CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    success_url = reverse_lazy("journal:journal_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    success_url = reverse_lazy("journal:journal_list")
    login_url = "users:login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class JournalDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaryEntry
    success_url = reverse_lazy("journal:journal_list")
    login_url = "users:login"
