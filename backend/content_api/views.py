from rest_framework import viewsets
from rest_framework.parsers import JSONParser  
from rest_framework.response import Response
from rest_framework import status
from .models import Content
from .serializers import ContentSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    
    def get_queryset(self):
        queryset = Content.objects.all()
        content_type = self.request.query_params.get('type', None)
        if content_type is not None:
            queryset = queryset.filter(type=content_type)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
