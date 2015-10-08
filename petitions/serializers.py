from django.conf import settings
import os
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from petitions.utils import generate_unique_upload_filename
from rest_framework import serializers
from petitions.models import Petition

IMAGES_UPLOAD_DIRECTORY = 'uploadedImages'


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


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):
        image_file = validated_data["image"]
        path = generate_unique_upload_filename(IMAGES_UPLOAD_DIRECTORY, 'jpg')
        default_storage.save(os.path.join(settings.MEDIA_ROOT, path), image_file)
        return path
