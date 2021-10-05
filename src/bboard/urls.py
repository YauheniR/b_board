from django.urls import path

from bboard.views import RegisterDoneView, user_activate
from bboard.views import RegisterUserView
from bboard.views import BBPasswordChangeView
from bboard.views import ChangeUserInfoView
from bboard.views import other_page
from bboard.views import BBLoginView
from bboard.views import profile
from bboard.views import BBLogoutView

from bboard.views import index

app_name = "bboard"

urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path("accounts/login/", BBLoginView.as_view(), name="login"),
    path("accounts/logout/", BBLogoutView.as_view(), name="logout"),
    path(
        "accounts/password/change/",
        BBPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/profile/change/", ChangeUserInfoView.as_view(), name="profile_change"
    ),
    path("accounts/profile/", profile, name="profile"),
    path("<str:page>/", other_page, name="other"),
    path("", index, name="index"),
]
