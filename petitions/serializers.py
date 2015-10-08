from django.contrib.auth.models import User
from rest_framework import serializers
from petitions.models import Petition, PetitionSign


class UserSerializer(serializers.HyperlinkedModelSerializer):
    petitions = serializers.PrimaryKeyRelatedField(many=True, queryset=Petition.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username')


class PetitionSignSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #petition = serializers.ReadOnlyField(source='petiton.id')
    class Meta:
        model = PetitionSign
        fields = ['petition', 'comment', 'anonymous', 'author']

class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    responsible = serializers.ReadOnlyField(source='responsible.username')
    signs = PetitionSignSerializer(many=True)
    class Meta:
        model = Petition
        fields = ('title', 'text', 'author', 'deadline', 'responsible', 'signs')
