# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
from location.models import Shop


@api_view(['GET'])
def section_a(request,list_num):
    print(Shop.objects(location='a'))
    print(type(list_num))
    print('section_a')
    return Response('section_a')

@api_view(['GET'])
def section_b(request,list_num):
    print('section_b')
    return Response('section_b')

@api_view(['GET'])
def section_c(request,list_num):
    print('section_c')
    return Response('section_c')

@api_view(['GET'])
def section_d(request,list_num):
    print('section_d')
    return Response('section_d')

@api_view(['GET'])
def section_e(request,list_num):
    print('section_e')
    return Response('section_e')