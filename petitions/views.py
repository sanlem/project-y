from django.conf import settings
from django.contrib.auth.models import User
from petitions.serializers import UserSerializerDetail, PetitionSerializerDetail, ImageUploadSerializer
from petitions.models import Petition
from rest_framework import viewsets, permissions, status
from petitions.permissions import IsAuthorOrReadOnly
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializerDetail


class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all().order_by('created_at')
    serializer_class = PetitionSerializerDetail
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ImageUploadViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    serializer_class = ImageUploadSerializer

    def create(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            path = serializer.save()
            image_url = request.build_absolute_uri("{}{}".format(settings.MEDIA_URL, path))
            return Response({"url": image_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
