from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from shop.models import Category, Product, Article

class ProductSerializer(ModelSerializer):
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    articles = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name','date_created','date_updated','category','articles']

    def get_articles(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.articles.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ArticleSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','name','date_created', 'date_updated','price','product']


"""class CategorySerializer(ModelSerializer):
    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','name','date_created','date_updated','products']"""


class CategorySerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']
class CategoryDetailSerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated','description']

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError('Category already exists')
        return value

    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
            # Levons une ValidationError si ça n'est pas le cas
            raise ValidationError('Name must be in description')
        return data
class ProductDetailSerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'articles'
    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'articles']

    def get_articles(self, instance):
        # Le paramètre 'instance' est l'instance du produit consulté.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les articles actifs
        queryset = instance.articles.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ArticleSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','ecoscore']

class ArticleListSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','name','date_created', 'date_updated','price','active','product']

    def validate_price(self, value):
        # Nous vérifions que la valeur du prix soit supérieure à 1 euro
        if value<=1:
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError('le prix doit etre supérieur à 1 euro')
        return value
    def validate_active(self, value):
        #nous vérifions que la valeur de active soit = True
        if  value is False:
            raise ValidationError('article non actif. merci de mettre le champ active à True')
        return value



class ArticleDetailSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','name','date_created', 'date_updated','price','product']