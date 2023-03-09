from django.urls import path
from . import views
from .views import send_email
from . import admin

urlpatterns=[
    path('',views.get_aln,name='get_aln'),
]
