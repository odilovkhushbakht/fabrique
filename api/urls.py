from django.urls import path

from api import views

urlpatterns = [
    path('client/<int:id>/', views.ClientView.as_view()),
    path('client/add/', views.ClientAddView.as_view()),
    path('client/update/', views.ClientUpdateView.as_view()),
    path('client/delete/<int:id>/', views.ClientDeleteView.as_view()),
    path('mailing/<int:clientId>/', views.MailingView.as_view()),
    path('mailing/add/', views.MailingAddView.as_view()),
    path('mailing/update/', views.MailingUpdateView.as_view()),
    # path('massage/<int:clientId>/', views.MessageView.as_view()),
    # path('massage/add/', views.MessageAddView.as_view()),
]
