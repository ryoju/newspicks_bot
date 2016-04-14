# -*- coding: utf-8 -*-

import Image
from StringIO import StringIO
import urllib2
from django.http import HttpResponse

def get_newspicks_image(news, width):
    try:
        url = get_image_url(news)
        buffer = urllib2.urlopen(url).read()
        img = Image.open(StringIO(buffer))
        size = (width, calculate_height(img.size[0], img.size[1], width))
        imger = img.resize(size)
        response = HttpResponse(content_type="image/png")
        imger.save(response, 'png')
        return response
    except urllib2.HTTPError:
        return HttpResponse(status=404)

def calculate_height(original_witdh, original_height, after_width):
    rate = float(original_height) / original_witdh
    after_height = int(after_width) * rate
    return int(after_height)

def has_image(news):
    try:
        url = get_image_url(news)
        buffer = urllib2.urlopen(url).read()
        return True
    except urllib2.HTTPError:
        return False

def get_image_url(news):
    return 'https://contents.newspicks.com/images/news/{0}/'.format(news)
