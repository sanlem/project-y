from django.contrib.auth.models import User
from petitions.serializers import UserSerializerDetail, PetitionSerializer
from petitions.models import Petition
from rest_framework import viewsets, permissions
from petitions.permissions import IsAuthorOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializerDetail


class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all().order_by('created_at')
    serializer_class = PetitionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
