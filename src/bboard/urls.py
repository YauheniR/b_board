from django.urls import path

from bboard.views import index

app_name = 'bboard'

urlpatterns = [
    path('', index, name='index')
]
