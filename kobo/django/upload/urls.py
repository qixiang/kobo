# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *

import kobo.django.upload.views


urlpatterns = [
    url(r"^$", kobo.django.upload.views.file_upload),
]
