from django.urls import path
from .views import UserViewRegister, UserViewLogin, logout_user, user_profile, UserProfileUpdate, user_profile_delete

urlpatterns = [
    
    path('register/', UserViewRegister.as_view(), name='signup'),
    path('login/', UserViewLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='user-profile'),
    path('profile/update/', UserProfileUpdate.as_view(), name='user-profile-update'),
    path('profile/delete/', user_profile_delete, name='user-profile-delete'),
]