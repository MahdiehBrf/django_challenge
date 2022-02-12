from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView 

from .models import Post, Form, FormResponse
from .serializer import PostSerializer, FormSerializer, FormResponseSerializer , BulkSerializer


class PostViewSet(viewsets.ViewSet):

    @action(methods=["get" ,"post"],detail=True , url_path="forms")
    def froms(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request ):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponseViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Form.objects.all()
        serializer = FormSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        title = request.data.pop('title')
        try:
            form = Form.objects.get(title=title)
            request.data['form'] = form.pk

        except:
            raise Exception('form is not valid')

        serializer = FormResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class BulkCreateView(APIView):
    def get(self , request):
        liss =list()
        serializer_class = BulkSerializer(liss , many = True)
        return Response(serializer_class.data)

    def post(self , request):
        serialized =BulkSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse({"bulk":"created"})
        
        else :
            return Response(serialized.errors , status= status.HTTP_400_BAD_REQUEST)









posts = [
    {
        "title": "test",
        "forms": {
            "title": "درخواست نمایندگی",
            "inputs": [
                {
                    "label": "شهر",
                    "type": "choice",
                    "choices": ["تهران", "مشهد", "تبریز"]
                }
            ],
            "extra_data": {
                "time_interval": 180
            }
        }
    },
    {
        "title": "test",
        "forms": {
            "title": "سفارش کوله",
            "inputs": [
                {
                    "label": "نام و نام خانوادگی",
                    "type": "string",
                }
            ],
            "extra_data": {
                "time_interval": 60
            }
        }
    }
]