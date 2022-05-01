from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logging/', views.logging, name='logging'),
    path('loggingout/', views.loggingout, name='loggingout'),
    path('subforum/<int:category>/', views.subforum, name='subforum'),
    path('reading/<int:id>/', views.reading, name='reading'),
    path('editing/<int:id>/', views.editing, name='editing'),
    path('deleting/<int:id>/', views.deleting, name='deleting'), # No template.
    path('profile/<int:id>/', views.profile, name='profile'),
]
