from django.contrib import admin

from .models import Post, Form, FormResponse

admin.site.register(Post)
admin.site.register(Form)
admin.site.register(FormResponse)
