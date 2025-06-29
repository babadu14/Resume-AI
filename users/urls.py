from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (UserListDetailViewSet, RegisterView, PasswordResetRequestViewSet, 
                    PasswordResetConfirmViewSet, CookieTokenObtainPairView,LogoutView)

router = DefaultRouter()

router.register('users', UserListDetailViewSet, basename='user')
router.register('register', RegisterView, basename='register')
router.register('password_reset', PasswordResetRequestViewSet, basename='password_reset')

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmViewSet.as_view({'post':'create'}), name='password_reset_confirm'),
    path('', include(router.urls)),
]