import json
import logging
import unittest
import sys
from django.contrib.auth import get_user_model
from petitions.models import Petition, Media, PetitionSign
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.conf import settings


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
        petition = PETITION.copy()
        petition.update({"media": []})
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.get_user())
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_media(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": [{"mediaUrl": "http://example.com/image.jpg", "type": "image"}]})

        count_before_post = len(Media.objects.all())
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(len(Media.objects.all()), count_before_post + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = json.loads(response.content.decode())
        self.assertEqual(response_data["media"][0]["mediaUrl"], "http://example.com/image.jpg")
        self.assertIn("id", response_data["media"][0])

    def test_change_media(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": [{"mediaUrl": "http://example.com/image.jpg", "type": "image"}]})

        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        response_data = json.loads(response.content.decode())
        created_media_id = response_data["media"][0]["id"]
        petition.update({
            "url": response_data["url"],
            "media": [{"id": created_media_id,
                       "mediaUrl": "http://example.com/changedImage.jpg", "type": "image"}]
        })

        count_before_post = len(Media.objects.all())
        response = self.client.put(response_data["url"], data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(Media.objects.all()), count_before_post)
        self.assertEqual(response_data["media"][0]["mediaUrl"], "http://example.com/changedImage.jpg")

    def test_add_media(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": []})

        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        response_data = json.loads(response.content.decode())
        petition.update({
            "url": response_data["url"],
            "media": [{"mediaUrl": "http://example.com/image.jpg", "type": "image"}]
        })

        count_before_post = len(Media.objects.all())
        response = self.client.put(response_data["url"], data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(Media.objects.all()), count_before_post + 1)
        self.assertEqual(response_data["media"][0]["mediaUrl"], "http://example.com/image.jpg")

    def test_no_add_media_with_id(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": []})

        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        response_data = json.loads(response.content.decode())
        petition.update({
            "url": response_data["url"],
            "media": [{"id": 42, "mediaUrl": "http://example.com/image.jpg", "type": "image"}]
        })

        response = self.client.put(response_data["url"], data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        petition = PETITION.copy()
        petition.update({"media": [{"id": 42, "mediaUrl": "http://example.com/image.jpg", "type": "image"}]})
        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_media(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": [{"mediaUrl": "http://example.com/image.jpg", "type": "image"}]})

        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        response_data = json.loads(response.content.decode())
        petition.update({
            "url": response_data["url"],
            "media": []
        })

        count_before_post = len(Media.objects.all())
        response = self.client.put(response_data["url"], data=petition, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(Media.objects.all()), count_before_post - 1)
        self.assertEqual(len(response_data["media"]), 0)

    def test_remove_petition(self):
        self.client.force_authenticate(self.get_user())
        petition = PETITION.copy()
        petition.update({"media": [{"mediaUrl": "http://example.com/image.jpg", "type": "image"}]})

        response = self.client.post(reverse('petition-list'), data=petition, format="json")
        response_data = json.loads(response.content.decode())

        petition_count_before_post = len(Petition.objects.all())
        media_count_before_post = len(Media.objects.all())

        response = self.client.delete(response_data["url"])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(len(Petition.objects.all()), petition_count_before_post - 1)
        self.assertEqual(len(Media.objects.all()), media_count_before_post - 1)

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

PETITION_SIGN = {
            "comment": "Whatever",
            "anonymous": "False",
        }

class TestPetitionSignResource(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        self.client.logout()
        response = self.client.get(reverse('petitionsign-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(response_data["results"]), len(PetitionSign.objects.all()))

    def test_detail(self):
        self.client.logout()
        petition = self.get_petition()
        sign = PetitionSign(author=self.get_users()[0], petition=petition, **PETITION_SIGN)
        sign.save()
        response = self.client.get(reverse('petitionsign-detail', args=[sign.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = json.loads(response.content.decode())
        self.assertTrue(isinstance(response_data["comment"], str))
        self.assertEqual(response_data["author"], sign.author.username)

    def test_creation(self):
        users = self.get_users()
        sign = self.set_sign_content()
        # trying to create with anonymous user
        self.client.logout()
        response = self.client.post(reverse("petitionsign-list"), data=sign, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # we use self.get_users[0] to create a sign in test_detail, so here we use another user
        self.client.force_authenticate(users[1])
        response = self.client.post(reverse("petitionsign-list"), data=sign, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_petition_status_updating_if_signs_goal_reached(self):
        PetitionSign.objects.all().delete()
        petition = self.get_petition()
        self.assertEqual(petition.status, "V")
        users = self.get_users()
        sign = self.set_sign_content()
        for user in users:
            self.client.logout()
            self.client.force_authenticate(user)
            response = self.client.post(reverse("petitionsign-list"), data=sign, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        signs = PetitionSign.objects.filter(petition=petition)
        self.assertEqual(len(users), len(signs))
        petition.refresh_from_db()
        self.assertEqual(petition.status, "A")

    # setting sign content. method was created to keep the code DRY
    @classmethod
    def set_sign_content(cls):
        petition = cls.get_petition()
        petition_url = "http://127.0.0.1:8000" + reverse('petition-detail', args=[petition.id])
        sign = PETITION_SIGN.copy()
        sign.update({"petition": petition_url})
        return sign    

    @classmethod
    def get_users(cls):
        # we should create as many users, as we need do reach goal of signs
        num = settings.SIGNS_GOAL
        if not hasattr(cls, "_users"):
            cls._users = []
            username = "testuser"
            for i in range(num):
                cls._users.append(get_user_model()(username=username + str(i)))
                cls._users[i].save()   
        return cls._users

    @classmethod
    def get_petition(cls):
        if not hasattr(cls, "_petition"):
            user = cls.get_users()[0]
            cls._petition = Petition(author=user, **PETITION)
            cls._petition.save()
        return cls._petition    
