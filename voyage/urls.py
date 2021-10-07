from django.urls import path

from . import views

urlpatterns = [
    path('', views.VoyageList.as_view()),
    path('scatterdf',views.VoyageScatterDF.as_view()),
    path('sunburstdf',views.VoyageSunburstDF.as_view())
    ]