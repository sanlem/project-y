from django.contrib.auth.models import User
from petitions.serializers import UserSerializer, PetitionSerializer, PetitionSignSerializer
from petitions.models import Petition, PetitionSign
from rest_framework import viewsets, permissions
from petitions.permissions import IsAuthorOrReadOnly
from rest_framework import status, filters


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all().order_by('created_at')
    serializer_class = PetitionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PetitionSignViewSet(viewsets.ModelViewSet):
    queryset = PetitionSign.objects.all()
    serializer_class = PetitionSignSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_fields = ('petition',)

    """
    def perform_create(self, serializer):
        
        Checking if current user had already signed this petition
        
        if PetitionSign.objects.all().filter(author=self.request.user).first() is None:
            
            serializer.save(author=self.request.user)
            print('saved')
        else:
            print('already signed')
    """