from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

class BackgroundApiView(generics.GenericAPIView):
    serializer_class = BackgroundSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = BackgroundSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
class BackgroundApiView1(generics.ListAPIView):
    serializer_class = BackgroundSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = self.model.objects.filter(pk=pk)
        return queryset
        
class BackgroundImageApiView(generics.GenericAPIView):
    serializer_class = BackgroundImageSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = BackgroundImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
class BackgroundImageApiView1(generics.ListAPIView):
    serializer_class = BackgroundImageSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = self.model.objects.filter(pk=pk)
        return queryset

class BackgroundColorApiView(generics.GenericAPIView):
    serializer_class = BackgroundColorSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = BackgroundColorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        

class BlogListApiView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    queryset = Blog.objects.all()
    
    lookup_field = 'slug'

# class CaregoryListApiView(generics.ListAPIView):
#     serializer_class = BlogListSerializer
#     queryset = Blog.objects.all()

class CaregoryListApiView(generics.GenericAPIView):
      
    serializer_class = BlogListSerializer
    model = serializer_class.Meta.model
    def get(self, request, slug, *args, **kwargs):
        # queryset = self.model.objects.filter(category_slug=slug)
        cat = Category.objects.get(slug=slug)
        queryset = self.model.objects.filter(category=cat)
        # print(queryset)
        serializer = BlogListSerializer(queryset, many=True)
        return Response(serializer.data)

        # return Response(queryset)

    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    lookup_field = 'slug'
    
class ContactApiView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
class Analytics(generics.ListAPIView):
    
    def get(self, request, *args, **kwargs):
        script = AnalyticsScript.objects.values_list('script', flat=True)[0]
        return Response({'script': script})