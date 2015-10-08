from datetime import datetime
import json
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


PETITION = {
    "title": "Build Death Star in KPI",
    "text": "We demand to build Death Star in the KPI",
    "deadline": "2015-09-01T12:00",
}


class TestPetitionsResource(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        petition = Petition(author=self.get_user(), **PETITION)
        petition.save()

        self.client.logout()
        response = self.client.get(reverse('petition-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode())
        self.assertTrue(isinstance(response_data["results"][0]["author"], dict))

    def test_detail(self):
        self.client.logout()
        petition = Petition(author=self.get_user(), **PETITION)
        petition.save()

        response = self.client.get(reverse('petition-detail', args=[petition.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode())
        self.assertTrue(isinstance(response_data["author"], dict))  # author is nested object

    def test_creation(self):
        self.client.logout()
        response = self.client.post(reverse('petition-list'), data=PETITION, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.get_user())
        response = self.client.post(reverse('petition-list'), data=PETITION, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def get_user(cls):
        if not hasattr(cls, "_user"):
            cls._user = get_user_model()(username="Luke")
            cls._user.save()
        return cls._user


class TestUserResource(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_detail(self):
        self.client.force_authenticate(self.get_staff_user())
        petition = Petition(author=self.get_staff_user(), **PETITION)
        petition.save()

        response = self.client.get(reverse('user-detail', args=[self.get_staff_user().id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode())
        self.assertTrue(isinstance(response_data["petitions"][0], dict))  # petition list consists of objects
        self.assertTrue("author" not in response_data["petitions"][0])  # petition should not contain author because
                                                                        # it's redundant info

    def test_detail_nopermissions(self):
        # possibly after auth implementation it will be changed!
        self.client.force_authenticate(self.get_user())
        response = self.client.get(reverse('user-detail', args=[self.get_user().id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_nopermissions_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('user-detail', args=[self.get_user().id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def get_staff_user(cls):
        if not hasattr(cls, "_staff_user"):
            cls._staff_user = get_user_model()(username="Leia", is_staff=True)  # only staff have access to user resource now
            cls._staff_user.save()
        return cls._staff_user

    @classmethod
    def get_user(cls):
        if not hasattr(cls, "_user"):
            cls._user = get_user_model()(username="Darth")
            cls._user.save()
        return cls._user
