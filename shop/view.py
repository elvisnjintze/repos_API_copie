from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer






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


class ProductViewSet2(ReadOnlyModelViewSet):
    """cette class permet l'accès à l'API (api/product) seulement en lecture
        pas de possibilité de créer, modifier et suprimer un produit"""
    serializer_class = ProductSerializer
    def get_queryset(self):
        #on applique le filtre; on veut tous produits dont l'attribut active=True
        queryset = Product.objects.filter(active=True)
        #vérifions la peésence de la variable category_id dans l'urls si c'est le cas
        #appliquons le filtre pour ne avoir que les produits de cette catégorie
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset




class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id:
            return queryset.filter(product_id=product_id)
        return queryset
