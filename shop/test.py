from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en
        # chaine de caractères sous le même format que celui de l’api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestCategory(ShopAPITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir
    # l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')
    def test_list(self):
        # Créons deux catégories dont une seule est active
        category = Category.objects.create(name='Fruits', active=True)
        category2 = Category.objects.create(name='Légumes', active=False)

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            }
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir
    # l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('product-list')

    def test_list(self):
        # Créons deux catégories dont une seule est active
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Elco', active=True, category=category)
        product2 = Product.objects.create(name='William', active=False, category=category)

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category.id
            }
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={'name': 'nouveau produit catégorie'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Product.objects.exists())