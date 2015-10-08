from django.contrib.auth.models import User
from rest_framework import serializers
from petitions.models import Petition


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class UserSerializerDetail(serializers.HyperlinkedModelSerializer):
    petitions = serializers.PrimaryKeyRelatedField(many=True, queryset=Petition.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username', 'petitions')


class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Petition
        fields = ('title', 'text', 'author', 'deadline', 'responsible')
