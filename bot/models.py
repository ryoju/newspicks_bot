# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
  name = models.CharField(max_length=32)
  mail = models.EmailField()

class Entry(models.Model):
  STATUS_DRAFT = "draft"
  STATUS_PUBLIC = "public"
  STATUS_SET = (
    (STATUS_DRAFT, "下書き"),
    (STATUS_PUBLIC, ",公開中"),
  )
  title = models.CharField(max_length=128)
  body = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(choices=STATUS_SET, default=STATUS_DRAFT, max_length=8)
  author = models.ForeignKey(User, related_name='entries')

