from django.contrib.auth.models import User
from rest_framework import serializers
from petitions.models import Petition


class UserSerializer(serializers.HyperlinkedModelSerializer):
    petitions = serializers.PrimaryKeyRelatedField(many=True, queryset=Petition.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username')


class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    responsible = serializers.ReadOnlyField(source='responsible.username')
    class Meta:
        model = Petition
        fields = ('title', 'text', 'author', 'deadline', 'responsible')
