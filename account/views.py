from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from account.models import *
from account.models import UserProfile as UserprofileModel
from account.serializers import UserProfileSerializer, CommentSerializer, \
    ServicesSerializer, ServiceRequestSerializer


# Create your views here.

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def registration_view(request, pk):
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['Resonse'] = "successfully regster new use"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class UserProfileAPIView(APIView):
    """UserProfile ApI view"""

    def get_object(self, id):
        try:
            userprofile = UserprofileModel.objects.get(id=id)
            return userprofile
        except UserprofileModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        userprofile = self.get_object(id)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)

    def put(self, request, id):
        userprofile = self.get_object(id)
        serializer = UserProfileSerializer(userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id):

        userprofile = self.get_object(id=id)
        userprofile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileModelViewSet(viewsets.ViewSet):
    def list(self, request):
        users = UserprofileModel.objects.all()
        serializer = UserProfileSerializer(users, many=True)

        return Response(serializer.data)


class UserLoginAPIView(ObtainAuthToken):
    '''Handle  creating user authrntication token '''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileViewSet(viewsets.ModelViewSet):
    '''handle creating and updating profile'''
    serializer_class = UserProfileSerializer
    queryset = UserprofileModel.objects.all()


class CommentModelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()





class ServicesSerializerModelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                     mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()


class ServiceRequestSerializerModelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                           mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()


class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        article = Comment.objects.filter(user_id=self.request.user.id)
        serializer = CommentSerializer(article, many=True)
        return Response(serializer.data)

    def create(self, request):
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceRequestViewSet(viewsets.ViewSet):

    def list(self, request):
        servicerequest = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(servicerequest, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ServiceRequest.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        serializer = ServiceRequestSerializer(service)
        return Response(serializer.data)

    def update(self,request,pk=None):
        service = ServiceRequest.objects.get(pk=pk)

