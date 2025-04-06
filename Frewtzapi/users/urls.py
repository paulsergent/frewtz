from django.urls import path
from .views import UserViewRegister, UserViewLogin

urlpatterns = [
    path('register/', UserViewRegister.as_view(), name='user-register'),
    path('login/', UserViewLogin.as_view(), name='user-login'),
    # path('logout/', UserViewLogout.as_view(), name='user-logout'),
    # path('profile/', UserViewProfile.as_view(), name='user-profile'),
    # path('profile/update/', UserViewProfileUpdate.as_view(), name='user-profile-update'),
    # path('profile/delete/', UserViewProfileDelete.as_view(), name='user-profile-delete'),
]