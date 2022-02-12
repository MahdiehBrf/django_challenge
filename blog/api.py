from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from .models import Post, Form, FormResponse
from .serializers import PostSerializer, FormSerializer, FormResponseSerializer


class PostViewSet(viewsets.ViewSet):

    @action(detail=True)
    def forms(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def create(self, request):
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