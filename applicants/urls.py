from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    path("interview", views.interview, name="interview"),
    path("document", views.document, name="document"),
    path('search_applicant/', views.search_applicant, name='search_applicant'),
]