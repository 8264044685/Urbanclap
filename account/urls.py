from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from account import views

router = DefaultRouter()

router.register('profileviewset', views.UserProfileViewSet)
router.register('CommentModelViewSet', views.CommentModelViewSet, basename='CommentModelViewSet')
router.register('ServicesSerializerModelViewSet', views.ServicesSerializerModelViewSet,
                basename='ServicesSerializerModelViewSet')
router.register('ServiceRequestSerializerModelViewSet', views.ServiceRequestSerializerModelViewSet,
                basename='ServiceRequestSerializerModelViewSet')

commentrouter = DefaultRouter()
commentrouter.register('CommentViewSet',views.CommentViewSet,basename='CommentViewSet')
commentrouter.register('CommentViewSet/<int:pk>',views.CommentViewSet,basename='CommentViewSet')

servicerequestrouter = DefaultRouter()
servicerequestrouter.register('ServiceRequestViewSet',views.ServiceRequestViewSet,basename='ServiceRequestViewSet')
servicerequestrouter.register('ServiceRequestViewSet/<int:pk>',views.ServiceRequestViewSet,basename='ServiceRequestViewSet')

urlpatterns = [
    path('', include(commentrouter.urls)),
    path('', include(servicerequestrouter.urls)),

    path('UserProfileView', views.UserProfileAPIView.as_view()),
    path('', include(router.urls)),
    path('register', views.registration_view, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('loginview', views.UserLoginAPIView.as_view()),
    path('userprofiledetailview/<int:id>', views.UserProfileAPIView.as_view()),
    # path('show_request', views.show_request,name='show_request'),


]
