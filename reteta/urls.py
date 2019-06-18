from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reteta import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('retete', views.RetetaViewSet)

app_name = 'reteta'

urlpatterns = [
    path('', include(router.urls))
]
