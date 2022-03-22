from django.urls import path
from apps.Auth.views import MyObtainTokenPairView, RegisterView, ProfileViewPost, ProfileViewGet
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile-post/', ProfileViewPost.as_view(), name='profile'),
    path('profile-update/<int:user_id>', ProfileViewGet.as_view(), name='profile')

]
