from django.urls import path
from . import views

urlpatterns = [
    path('', views.scaffold_component_list, name='scaffold_component_list'),
    path('create/', views.scaffold_component_create, name='scaffold_component_create'),
    path('<int:pk>/', views.scaffold_component_detail, name='scaffold_component_detail'),
    path('<int:pk>/edit/', views.scaffold_component_edit, name='scaffold_component_edit'),
    path('<int:pk>/delete/', views.scaffold_component_delete, name='scaffold_component_delete'),
]