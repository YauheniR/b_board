from django.urls import include
from django.urls import path
from users.views import BBLoginView
from users.views import BBLogoutView
from users.views import BBPasswordChangeView
from users.views import ChangeUserInfoView
from users.views import DeleteUserView
from users.views import profile
from users.views import RegisterDoneView
from users.views import RegisterUserView
from users.views import user_activate

app_name = "users"
urlpatterns = [
    path(
        "register/",
        include(
            [
                path(
                    "activate/<str:sign>/",
                    user_activate,
                    name="register_activate",
                ),
                path("done/", RegisterDoneView.as_view(), name="register_done"),
                path("", RegisterUserView.as_view(), name="register"),
            ]
        ),
    ),
    path(
        "profile/",
        include(
            [
                path(
                    "change/",
                    ChangeUserInfoView.as_view(),
                    name="profile_change",
                ),
                path("delete/", DeleteUserView.as_view(), name="profile_delete"),
                path("", profile, name="profile"),
            ]
        ),
    ),
    path("login/", BBLoginView.as_view(), name="login"),
    path("logout/", BBLogoutView.as_view(), name="logout"),
    path(
        "password/change/",
        BBPasswordChangeView.as_view(),
        name="password_change",
    ),
]
