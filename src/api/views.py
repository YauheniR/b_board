from api.serializers import BbDetailSerializer
from api.serializers import BbSerializer
from api.serializers import CommentSerializer
from bboard.models import Bb
from comments.models import Comment
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST


@api_view(["GET"])
def bbs(request):
    if request.method == "GET":
        bbs = Bb.objects.filter(is_active=True)[:10]
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comment = Comment.objects.filter(is_active=True, bb=pk)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer
