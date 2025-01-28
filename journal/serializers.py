from rest_framework import serializers

from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = ["id", "title", "content", "created_at", "owner"]
        read_only_fields = ["created_at", "owner"]
