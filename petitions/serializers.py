from django.contrib.auth.models import User
from rest_framework import serializers
from petitions.models import Petition


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Petition
        fields = ('url', 'title', 'text', 'deadline', 'responsible')


class UserSerializerDetail(UserSerializer):
    petitions = PetitionSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('petitions',)


class PetitionSerializerDetail(PetitionSerializer):
    author = UserSerializer(read_only=True)
    class Meta(PetitionSerializer.Meta):
        fields = PetitionSerializer.Meta.fields + ('author',)
