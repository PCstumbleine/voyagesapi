from django.urls import path

from . import views

urlpatterns = [
    path('', views.VoyageView.as_view()),
    path('by_id/<int:id>',views.VoyageByID.as_view()),
    path('min_number_disembarked/<int:imp_total_num_slaves_disembarked>',views.VoyageByMinDisembarked.as_view())
]