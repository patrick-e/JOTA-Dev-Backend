from rest_framework import serializers
from .models import News


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('autor',)

    def create(self, validated_data):
        # Associa o autor autenticado à notícia
        validated_data['autor'] = self.context['request'].user
        return super().create(validated_data)

    def validate_titulo(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Título deve ter pelo menos 5 caracteres")
        return value

    def validate_conteudo(self, value):
        if len(value) < 50:
            raise serializers.ValidationError("Conteúdo deve ter pelo menos 50 caracteres")
        return value

    def validate_categoria(self, value):
        if value not in [choice[0] for choice in News.CATEGORY_CHOICES]:
            raise serializers.ValidationError("Categoria inválida")
        return value

    def validate_status(self, value):
        if value not in [choice[0] for choice in News.STATUS_CHOICES]:
            raise serializers.ValidationError("Status inválido")
        return value

    def validate_acesso(self, value):
        if value not in [choice[0] for choice in News.ACCESS_CHOICES]:
            raise serializers.ValidationError("Tipo de acesso inválido")
        return value
