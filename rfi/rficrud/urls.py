from django.urls import path, include
from . import views
from.views import DefaultSignersConstructionViewSet, \
    RFIViewSet, ProjectViewSet, CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter
from .autocomplete import ObjectAutocomplete
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
app_name = 'rficrud'

#Содержит все пути для отображения только на ознакомление с информацией

router = DefaultRouter()
router.register('defualt-signers', DefaultSignersConstructionViewSet, basename='defualt-signers')
router.register(r'rfis', RFIViewSet, basename='rfis')
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', views.mainpage, name='index'),
    path('rfi_list/', views.rfi_list, name="rfi_list"),
    path('get_projects_by_object/<int:object_id>/', views.get_projects_by_object, name='get_projects_by_object'),
    #path('slug_create', views.slug_create, name='slug_create'),
    path('rfi_list/<slug:rfi_slug>/', views.single_rfi_read, name='single_rfi_read'),
    path('rfi_list/<slug:rfi_slug>/add_comment/', views.add_comment, name='add_comment'),
    path('update_status/<int:rfi_id>/<str:new_status>/', views.update_rfi_status, name='update_rfi_status'),
    path('inspector/<str:username>/', views.inspector_view, name='inspector_view'),
    path('search/', views.search, name="search"),
    path('rfi_create/', views.RFICreateView.as_view(), name='rfi_create'),
    path('object_autocomplete/', ObjectAutocomplete.as_view(), name='object_autocomplete'),
    path('api/', include(router.urls)),
    #path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair')
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]