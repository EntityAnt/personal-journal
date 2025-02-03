from django.forms import BooleanField, ImageField, ModelForm, HiddenInput, CharField
from django.urls import reverse_lazy

from journal.models import DiaryEntry
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            elif isinstance(fild, ImageField):
                fild.widget.attrs["class"] = "form-control-file"
            else:
                fild.widget.attrs["class"] = "form-control"


class DiaryEntryForm(StyleFormMixin, ModelForm):
    class Meta:
        model = DiaryEntry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Ограничиваем queryset для поля owner
            if not self.user.is_superuser:
                # Для обычных пользователей показываем только их самих
                self.fields['owner'].queryset = User.objects.filter(id=self.user.id)
                # Делаем поле скрытым
                self.fields['owner'].widget = HiddenInput()
            else:
                # Для суперпользователей показываем всех пользователей
                self.fields['owner'].queryset = User.objects.all()

            # Устанавливаем текущего пользователя как владельца по умолчанию
            self.fields['owner'].initial = self.user

    def save(self, commit=True):
        diary_entry = super().save(commit=False)
        if self.user.is_superuser:
            diary_entry.owner = self.cleaned_data['owner']
        else:
            diary_entry.owner = self.user
        if commit:
            diary_entry.save()
        return diary_entry
