from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("safety-walk/", views.safetywalk_list, name="safetywalk_list"),
    path("safety-walk/new/", views.safetywalk_create, name="safetywalk_create"),
    path("safety-walk/<int:pk>/",views.safetywalk_detail,name="safetywalk_detail",
),

]
