from rest_framework import serializers
from .models import Pessoas

class BuscaSerializer(serializers.Serializer):
    nome = serializers.CharField()


class InsereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = "__all__"
