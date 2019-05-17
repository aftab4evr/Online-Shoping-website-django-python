# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(PointOfInterest)
admin.site.register(SingUp)
admin.site.register(ProductChoice)