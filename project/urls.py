from django.contrib import admin
from django.urls import path, include
from shop.view import CategoryViewSet2, ProductViewSet2
from shop.view import ArticleViewSet, AdminCategoryViewSet, AdminArticleViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


#ceci est la route permettant d'accéder à une API seulement en lecture
router2 = routers.SimpleRouter()

# Puis lui déclarons une url basée sur le mot clé ‘category2’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category2/’
router2.register('category', CategoryViewSet2, basename='category')
product2route = routers.SimpleRouter()
articlerouter = routers.SimpleRouter()
articlerouter.register('article',ArticleViewSet, basename='article')
product2route.register('product', ProductViewSet2, basename='product')
admin_router_category = routers.SimpleRouter()
admin_router_category.register('admin/category',AdminCategoryViewSet, basename='admin-category')
admin_router_article = routers.SimpleRouter()
admin_router_article.register('admin/article',AdminArticleViewSet, basename='admin-article')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include(router2.urls)),
    path('api/',include(product2route.urls)),
    path('api/',include(articlerouter.urls)),
    path('api/',include(admin_router_category.urls)),
    path('api/',include(admin_router_article.urls)),
    path('api/token',TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='refresh_token')
]
