from django.urls import path

from api import views

urlpatterns = [
    path('client/<int:id>/', views.ClientView.as_view()),
    path('client/add/', views.ClientAddView.as_view()),
    path('client/update/', views.ClientUpdateView.as_view()),
    path('client/delete/<int:id>/', views.ClientDeleteView.as_view()),
]
