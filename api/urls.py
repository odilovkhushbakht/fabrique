from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from api import views

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Mailing API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('client/<int:id>/', views.ClientView.as_view()),
    path('client/add/', views.ClientAddView.as_view()),
    path('client/add/many/', views.ClientAddManyView.as_view()),
    path('client/update/', views.ClientUpdateView.as_view()),
    path('client/delete/<int:id>/', views.ClientDeleteView.as_view()),
    path('mailing/', views.MailingListView.as_view()),
    path('mailing/<int:id>/', views.MailingView.as_view()),
    path('mailing/add/', views.MailingAddView.as_view()),
    path('mailing/update/<int:id>/', views.MailingUpdateView.as_view()),
    path('task/run/<int:id>/', views.TaskRunView.as_view()),
    path('task/abort/<slug:id>/', views.TaskAbortView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:id>/', views.OrderDetailView.as_view()),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),

]
