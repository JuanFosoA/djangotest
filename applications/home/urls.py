from django.urls import path
from . import views

app_name = "home_app"

urlpatterns = [
    path("home/", views.IndexView.as_view()),
    path("lista/", views.PruebaListView.as_view()),
    path("pruebas/", views.ModeloPruebaListView.as_view()),
    path("add/", views.PruebaCreateView.as_view(), name="prueba_add"),
    path(
        "resume-foundation/",
        views.ResumeFoundationView.as_view(),
        name="resume_foundation",
    ),
]
