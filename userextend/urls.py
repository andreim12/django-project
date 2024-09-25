from django.urls import path

from userextend import views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view(), name='create-user'),
    path('activate/<uid64>/<token>/', views.activate_user, name='activate'),
    path('user_history/', views.UserHistoryListView.as_view(), name='user-history')
]
