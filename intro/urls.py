from django.urls import path

from intro import views

urlpatterns = [
    path('ceva/', views.index, name='first-page'),
    path('another/', views.another_page, name='second-page'),
    path('list_of_cars/', views.cars, name='list-of-cars'),
    path('football/', views.football, name='football-players'),
    path('data/', views.get_data, name='data')
]
