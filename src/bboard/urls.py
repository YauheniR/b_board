from django.urls import path

from bboard.views import other_page
from bboard.views import BBLoginView
from bboard.views import profile
from bboard.views import BBLogoutView

from bboard.views import index

app_name = "bboard"

urlpatterns = [
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path("<str:page>/", other_page, name="other"),
    path("", index, name="index"),
]
