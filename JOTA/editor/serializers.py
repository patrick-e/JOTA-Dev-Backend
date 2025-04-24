from rest_framework import serializers
from .models import News

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def update(self, instance, validated_data):
        # Se a imagem não for fornecida, mantenha a imagem existente
        imagem = validated_data.pop('imagem', None)
        if imagem:
            instance.imagem = imagem

        # Atualize os outros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance