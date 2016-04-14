# -*- coding: utf-8 -*-

import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from image.functions import get_newspicks_image

class NewsPicksImageView(View):
    http_method_names = ['get', 'post']

    def get(self, *args, **kwargs):
        news = kwargs['news']
        width = kwargs.get('width', 1040)
        print news
        print width
        return get_newspicks_image(news, int(width))

    def post(self, request, *args, **kwargs):
        print args
        print kwargs
        return JsonResponse({'status': 'post'})

