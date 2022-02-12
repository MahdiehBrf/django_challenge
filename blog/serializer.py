import json
from django.http import JsonResponse , HttpResponse
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework import status

from .models import Form, FormResponse, Post


class FormSerializer(serializers.ModelSerializer):
    inputs = serializers.JSONField()

    class Meta:
        model = Form
        fields = ['title', 'inputs', 'extra_data']


class PostSerializer(serializers.ModelSerializer):
    forms = FormSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'forms']

    def create(self, validated_data):
        forms_data = validated_data.pop('forms')
        post, created = Post.objects.get_or_create(**validated_data)
        for form_data in forms_data:
            inputs = form_data.pop('inputs')
            inputs = json.dumps(inputs)
            form_data['inputs'] = inputs
            form, created = Form.objects.get_or_create(post=post, **form_data)
            print(form , created)
        return post


class FormResponseSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = FormResponse
        fields = ['form', 'data']
        
        

class BulkSerializer(serializers.Serializer):
    posts = serializers.ListField()
    
    
    def create(self, validated_data):
        
        
        for elm in validated_data.get("posts"):

            forms_data = elm.pop('forms')
            post, created = Post.objects.get_or_create(**elm)

            form, created = Form.objects.get_or_create(post=post, **forms_data)
        
