from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reteta import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'reteta'

urlpatterns = [
    path('', include(router.urls))
]
