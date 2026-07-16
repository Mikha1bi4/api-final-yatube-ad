from django.urls import include, path
from rest_framework import routers
from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    path('v1/jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/comments/', CommentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        })),
    path(
        'v1/posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'})
    ),
    path('v1/follow/', FollowViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    ))
]
