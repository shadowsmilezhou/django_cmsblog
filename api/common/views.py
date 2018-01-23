# -*- coding:utf-8 -*-
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,reverse,redirect
from django.core.cache import cache

from utils.captcha.xtcaptcha import Captcha
from PIL import Image

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

def captcha(request):
    text,image = Captcha.gene_code()
    #image.save('text.png','png')
 ##    return HttpResponse(text)
    out = StringIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    # key = text.lower()
    # value = key
    # cache.set(key,value,120)
    return response