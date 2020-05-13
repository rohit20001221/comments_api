from django.contrib import admin
from .models import WebSite, Comment, Like, DisLike
# Register your models here.
admin.site.register(WebSite)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(DisLike)
