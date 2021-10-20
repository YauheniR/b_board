from api.views import BbDetailView
from api.views import bbs
from api.views import comments
from django.urls import path

urlpatterns = [
    path("bbs/<int:pk>/comments/", comments),
    path("bbs/<int:pk>/", BbDetailView.as_view()),
    path("bbs/", bbs),
]
