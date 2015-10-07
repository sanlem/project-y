from datetime import datetime
import logging
import unittest
import sys
from django.contrib.auth import get_user_model
from petitions.models import Petition
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestPetitionsApi(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        self.client.logout()
        response = self.client.get(reverse('petition-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        self.client.logout()
        petition = Petition(title="Build Death Star in KPI", text="We demand to build Death Star in the KPI",
                     deadline=datetime.now(), author=self.get_user())
        petition.save()

        response = self.client.get(reverse('petition-detail', args=[petition.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation(self):
        petition = {
            "title": "Build Death Star in KPI",
            "text": "We demand to build Death Star in the KPI",
            "deadline": "2015-09-01T12:00",
        }
        self.client.logout()
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.get_user())
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def get_user(cls):
        if not hasattr(cls, "_user"):
            cls._user = get_user_model()(username="Luke")
            cls._user.save()
        return cls._user
