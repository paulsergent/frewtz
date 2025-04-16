from django.urls import path
from .views import UserViewRegister, UserViewLogin, logout_user

urlpatterns = [
    
    path('register/', UserViewRegister.as_view(), name='signup'),
    path('login/', UserViewLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # path('logout/', UserViewLogout.as_view(), name='user-logout'),
    # path('profile/', UserViewProfile.as_view(), name='user-profile'),
    # path('profile/update/', UserViewProfileUpdate.as_view(), name='user-profile-update'),
    # path('profile/delete/', UserViewProfileDelete.as_view(), name='user-profile-delete'),
]