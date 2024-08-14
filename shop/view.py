from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer
from shop.serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction





class CategoryViewSet2(ReadOnlyModelViewSet):
    """cette class permet l'accès à l'API (api/category2) seulement en lecture
    pas de possibilité de créer, modifier et suprimer une catégorie"""
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    def get_queryset(self):
        #return Category.objects.all()
        queryset = Category.objects.filter(active=True)
        return queryset
    def get_serializer_class(self):
        #si l'action démandée est retrieve cad demander de lister un détail sur
        # une catégory donnée par exple api/category/3
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @transaction.atomic
    @action(detail=True, methods=['POST'])
    def desable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        category = self.get_object()
        category.active = False
        category.save()

        # Puis désactivons les produits de cette catégorie
        category.products.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()


class ProductViewSet2(ReadOnlyModelViewSet):
    """cette class permet l'accès à l'API (api/product) seulement en lecture
        pas de possibilité de créer, modifier et suprimer un produit"""
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    def get_queryset(self):
        #on applique le filtre; on veut tous produits dont l'attribut active=True
        queryset = Product.objects.filter(active=True)
        #vérifions la peésence de la variable category_id dans l'urls si c'est le cas
        #appliquons le filtre pour ne avoir que les produits de cette catégorie
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()




class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id:
            return queryset.filter(product_id=product_id)
        return queryset
