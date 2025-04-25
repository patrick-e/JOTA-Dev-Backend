from rest_framework import serializers
from .models import News

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        # Associa o autor autenticado à notícia
        validated_data['autor'] = self.context['request'].user
        return super().create(validated_data)