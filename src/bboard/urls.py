from bboard.views import by_rubric
from bboard.views import index
from bboard.views import other_page
from django.urls import path

app_name = "bboard"

urlpatterns = [
    path("<int:pk>/", by_rubric, name="by_rubric"),
    path("<str:page>/", other_page, name="other"),
    path("", index, name="index"),
]
