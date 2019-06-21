from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import Reteta, Tag, Ingredient
from reteta.serializers import RetetaSerializer, RetetaDetailSerializer

RETETA_URL = reverse('reteta:reteta-list')
# /api/reteta/retete
# /api/reteta/retete/1/


def detail_url(reteta_id):
    """"Return reteta detail URL"""
    return reverse('reteta:reteta-detail', args=[reteta_id])


def sample_tag(user, name='Main course'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinemon'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_reteta(user, **params):
    """Create and return a sample reteta"""
    defaults = {
        'title': 'Sample reteta',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)
    return Reteta.objects.create(user=user, **defaults)


class PublicRetetaApiTests(TestCase):
    """Test unauthenticated reteta API access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required"""
        res = self.client.get(RETETA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRetetaApiTests(TestCase):
    """Test the authorized user reteta API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@chris.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_reteta_list(self):
        """Test retrieving a list of retete"""
        sample_reteta(user=self.user)
        sample_reteta(user=self.user)

        res = self.client.get(RETETA_URL)

        retete = Reteta.objects.all().order_by('-id')
        serializer = RetetaSerializer(retete, many=True)  # return list
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_reteta_limited_to_user(self):
        """Test that reteta returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@chris.com',
            'testpass'
        )
        sample_reteta(user=user2)
        sample_reteta(user=self.user)

        res = self.client.get(RETETA_URL)
        rete = Reteta.objects.filter(user=self.user)
        serializer = RetetaSerializer(rete, many=True)  # return list
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_reteta_detail(self):
        """"Test viewinng a reteta detail"""
        reteta = sample_reteta(user=self.user)
        reteta.tags.add(sample_tag(user=self.user))
        reteta.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(reteta.id)
        res = self.client.get(url)
        serializer = RetetaDetailSerializer(reteta)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_reteta(self):
        """Test creating reteta"""
        payload = {
            'title': 'Meat Feast',
            'time_minutes': 30,
            'price': 2.50
        }
        res = self.client.post(RETETA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reteta = Reteta.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(reteta, key))

    def test_create_reteta_with_tags(self):
        """test_create_reteta_with_tags"""
        tag1 = sample_tag(user=self.user, name='Vegetarian')
        tag2 = sample_tag(user=self.user, name='Sizller')
        payload = {
            'title': 'Hawaian',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RETETA_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reteta = Reteta.objects.get(id=res.data['id'])
        tags = reteta.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_reteta_with_ingredients(self):
        """test_create_reteta_with_tags"""
        ingredient1 = sample_ingredient(user=self.user, name='Onion')
        ingredient2 = sample_ingredient(user=self.user, name='Sweetcorn')
        payload = {
            'title': 'Fajita',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 2,
            'price': 2.50
        }
        res = self.client.post(RETETA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reteta = Reteta.objects.get(id=res.data['id'])
        ingredients = reteta.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
