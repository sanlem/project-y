from django.conf import settings
from django.utils.functional import cached_property
import os
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from petitions.utils import generate_unique_upload_filename
from rest_framework import serializers
from petitions.models import Petition, Media, PetitionSign, Tag
from rest_framework.fields import empty
from rest_framework.reverse import reverse
from django.core.exceptions import ObjectDoesNotExist


IMAGES_UPLOAD_DIRECTORY = 'uploadedImages'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class PetitionSignSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #petition = serializers.ReadOnlyField(source='petiton.id')
    class Meta:
        model = PetitionSign
        fields = ['petition', 'comment', 'anonymous', 'author']


class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    signs = serializers.SerializerMethodField()

    def get_signs(self, obj):
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError("Request is not in context of serializer")
        return request.build_absolute_uri(reverse('petitionsign-list') + '?petition=' + str(obj.id))

    status = serializers.ReadOnlyField()
    sign_count = serializers.ReadOnlyField(source='signs.count')
    class Meta:
        model = Petition
        fields = ('url', 'title', 'text', 'deadline', 'responsible', 'signs', 'status', 'sign_count')


class UserSerializerDetail(UserSerializer):
    petitions = PetitionSerializer(many=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('petitions',)


class MediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    class Meta:
        model = Media
        fields = ('id', 'mediaUrl', 'type')


class TagSlugRelatedField(serializers.SlugRelatedField):
    """ 
        Default field searches for every instance
        in existing queryset, but we need to create object
        if it doesn't exists in queryset, not to throw error.
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            new_tag = Tag.objects.create(**{self.slug_field: data})
            return new_tag
        except (TypeError, ValueError):
            self.fail('invalid')


class PetitionSerializerDetail(PetitionSerializer):
    author = UserSerializer(read_only=True)
    media = MediaSerializer(many=True)
    tags = TagSlugRelatedField(
        many=True, 
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta(PetitionSerializer.Meta):
        fields = PetitionSerializer.Meta.fields + ('author', 'media', 'tags')

    def create(self, validated_data):
        media_data = validated_data.pop('media')

        tags_data = validated_data.pop('tags')

        petition = Petition.objects.create(**validated_data)
        for media_item in media_data:
            if 'id' in media_item:
                raise serializers.ValidationError("Don't add new media with id field")
            Media.objects.create(petition=petition, **media_item)

        for tag_item in tags_data:
            tag = Tag.objects.get(name=tag_item)
            petition.tags.add(tag)
        petition.save()

        return petition

    def update(self, instance, validated_data):
        if 'media' in validated_data: # for PATCH request
            media_data = validated_data.pop('media')
            updated_media_ids = set(obj['id'] for obj in media_data if 'id' in obj)
            existing_media_ids = set(obj.id for obj in instance.media.all())

            new_media = updated_media_ids.difference(existing_media_ids)
            if len( updated_media_ids.intersection(new_media) ) != 0:
                raise serializers.ValidationError("Don't add new media with id field")

            # update existing items and add new
            for media_item_data in media_data:
                if 'id' in media_item_data:
                    media_instance = Media.objects.get(pk=media_item_data['id'])
                    existing_media_ids.remove(media_item_data['id'])
                else:
                    media_instance = Media()
                media_instance.petition = instance
                for attr, value in media_item_data.items():
                    setattr(media_instance, attr, value)
                media_instance.save()

            # remove deleted items
            deleted_items = existing_media_ids
            for deleted_item_id in deleted_items:
                Media.objects.filter(pk=deleted_item_id).delete()
        
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            updated_tags = set(tags_data)
            existing_tags = set(obj.name for obj in instance.tags.all())

            keeped_tags = existing_tags.intersection(updated_tags)
            deleted_tags = existing_tags.difference(keeped_tags)
            new_tags = updated_tags.difference(existing_tags)
            for tag_name in new_tags:
                tag = Tag.objects.get(name=tag_name)
                instance.tags.add(tag)

            for tag_name in deleted_tags:
                tag = Tag.objects.get(name=tag_name)
                instance.tags.remove(tag)

            instance.save()

        return super().update(instance, validated_data)


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):
        image_file = validated_data["image"]
        path = generate_unique_upload_filename(IMAGES_UPLOAD_DIRECTORY, 'jpg')
        default_storage.save(os.path.join(settings.MEDIA_ROOT, path), image_file)
        return path
