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
    
    def update_by_type(self, request):
        content_type = request.data.get('type', None)
        if not content_type:
            return Response({"error": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(type=content_type) 
        except Content.MultipleObjectsReturned:
            return Response({"error": "Multiple records found, use a more specific filter"}, status=status.HTTP_400_BAD_REQUEST)
        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(content, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_by_type(self, request):
        content_type = request.data.get('type', None)
        if not content_type:
            return Response({"error": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Content.objects.filter(type=content_type).delete()
        if deleted_count == 0:
            return Response({"error": "No matching content found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"{deleted_count} content(s) deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
