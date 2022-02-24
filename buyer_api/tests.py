from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import tag
from django.urls import reverse
from shop.models import *
from model_mommy import mommy

User = get_user_model()


class TestShopListView(APITestCase):

    def setUp(self):
        self.admin = mommy.make(User)
        self.seller = mommy.make(User)
        self.buyer = mommy.make(User)
        mommy.make(Shop, status='P', owner=self.seller, _quantity=10)
        mommy.make(Shop, status='C', owner=self.seller, _quantity=10)
        mommy.make(Shop, status='D', owner=self.seller, _quantity=10)
        mommy.make(ShopType, author=self.admin, _quantity=5)
        mommy.make(Category, author=self.seller, _quantity=2)

    def test_shop_list(self):
        url = reverse('shop_list_api')
        self.client.force_authenticate(self.buyer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 10)
        self.assertEqual(Shop.objects.count(), 30)


class TestShopTypeListView(APITestCase):

    def setUp(self):
        self.admin = mommy.make(User, is_staff=True)
        self.buyer = mommy.make(User)
        mommy.make(ShopType, author=self.admin, _quantity=5)

    def test_shop_type_list(self):
        url = reverse('shop_type_list_api')
        self.client.force_authenticate(self.buyer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 5) 


class TestShopCategoryListView(APITestCase):

    def setUp(self):
        self.admin = mommy.make(User)
        self.seller = mommy.make(User)
        self.buyer = mommy.make(User)
        self.shop_type = mommy.make(ShopType, author=self.admin)
        self.shop = mommy.make(Shop, status='C', type=self.shop_type, owner=self.seller)
        mommy.make(Category, author=self.seller, _quantity=10)

    def test_category_list(self):
        url = reverse('shop_category_list_api', kwargs={'shop_slug': self.shop.slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 10) 
        self.assertEqual(Category.objects.count(), 10)


class TestShopProductListView(APITestCase):

    def setUp(self):
        self.admin = mommy.make(User)
        self.seller = mommy.make(User)
        self.buyer = mommy.make(User)
        self.shop_type = mommy.make(ShopType, author=self.admin)
        self.shop = mommy.make(Shop, status='C', type=self.shop_type, owner=self.seller)
        self.category = mommy.make(Category, author=self.seller)
        mommy.make(Product, owner=self.seller, shop=self.shop,
                    category=self.category, price=500, _quantity=10)

    def test_shop_product_list(self):
        url = reverse('shop_product_List_api', kwargs={'shop_slug': self.shop.slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 10) 

