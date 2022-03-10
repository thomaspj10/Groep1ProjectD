from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('map', views.FoliumView.as_view() , name='map'),
    path('graphs/', views.graphs, name='graphs'),
    path('diagrams/', views.diagrams, name='diagrams'),
    path('load_excel/', views.load_excel, name='load_excel'),
    path('load_api_data/', views.load_api_data, name='load_api_data'),
    path('load_db_data/', views.load_db, name='load_db_data'),
    path('filter_data/', views.filter_data, name='filter_data'),
]
