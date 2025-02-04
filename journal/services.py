from django.core.cache import cache
from django.db.models import Q

from config.settings import CACHE_ENABLE
from journal.models import DiaryEntry


def get_entry_from_cache(user, search_query=""):
    """Получение данных по записям из кэша, если кэш пуст, берем из БД."""
    if not CACHE_ENABLE:
        return DiaryEntry.objects.all()

    # Создаем уникальный ключ для кэша
    key = f"journal_list_{user.id}_{search_query}"
    cache_data = cache.get(key)

    if cache_data is not None:
        return cache_data

    # Если кэша нет, получаем данные из БД
    if user.is_superuser:
        cache_data = DiaryEntry.objects.all()
    else:
        cache_data = DiaryEntry.objects.filter(owner=user)

    # Поиск по заголовку и контенту
    if search_query:
        cache_data = cache_data.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    cache.set(key, cache_data)

    return cache_data
