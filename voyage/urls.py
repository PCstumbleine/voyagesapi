from django.urls import path

from . import views

urlpatterns = [
    path('', views.VoyageList.as_view()),
    path('table',views.VoyageScatterDF.as_view())
    ]