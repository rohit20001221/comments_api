from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .serializers import CommentSerializer
from .models import *
# Create your views here.


def create_website(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        name = request.POST.get('name')
        site_url = request.POST.get('site_url')

        if WebSite.objects.filter(site_url=site_url).exists():
            messages.error(request, 'website url already exists')
            return redirect('home')
        else:
            website = WebSite.objects.create(name=name, site_url=site_url)
            messages.success(request, f"created the website successful your key is {website.key}")
            return redirect('home')



class CommentListView(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_website(self, key):
        try:
            web_site = WebSite.objects.get(key=key)
        except:
            raise Http404

        return web_site

    def get(self, request, key):
        print(key)
        web_site = self.get_website(key)

        comments = web_site.comments_set.filter(is_root=True)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, key):
        web_site = self.get_website(key)

        print(request.data)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, website=web_site)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCommentView(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_website(self, key):
        try:
            web_site = WebSite.objects.get(key=key)
        except:
            raise Http404

        return web_site


    def get_comment(self, pk):
        try:
            object = Comment.objects.get(pk=pk)
        except:
            raise Http404

        return object

    def get(self, request, key, pk):
        comment = self.get_comment(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, key, pk):
        comment = self.get_comment(pk)
        website = self.get_website(key)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(sub_comment=comment, website=website, user=request.user, is_root=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_website(self, key):
        try:
            web_site = WebSite.objects.get(key=key)
        except:
            raise Http404

        return web_site


    def get_comment(self, pk):
        try:
            object = Comment.objects.get(pk=pk)
        except:
            raise Http404

        return object

    def post(self, request, key, pk):
        website = self.get_website(key)
        comment = self.get_comment(pk)

        serializer = LikeSerializer()

        if DisLike.objects.filter(user=request.user, comment=comment).exists():
            DisLike.objects.filter(user=request.user, comment=comment).first().delete()

        serializer.save(user=request.user,comment=comment)
        return Response({'liked':'ok'}, status=status.HTTP_200_OK)

class DisLikeView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_website(self, key):
        try:
            web_site = WebSite.objects.get(key=key)
        except:
            raise Http404

        return web_site


    def get_comment(self, pk):
        try:
            object = Comment.objects.get(pk=pk)
        except:
            raise Http404

        return object

    def post(self, request, key, pk):
        website = self.get_website(key)
        comment = self.get_comment(pk)

        serializer = DisLikeSerializer()

        if Like.objects.filter(user=request.user, comment=comment).exists():
            Like.objects.filter(user=request.user, comment=comment).first().delete()

        serializer.save(user=request.user,comment=comment)
        return Response({'liked':'ok'}, status=status.HTTP_200_OK)
