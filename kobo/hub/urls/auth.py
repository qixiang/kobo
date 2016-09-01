# -*- coding: utf-8 -*-


from django.conf.urls import url

import kobo.hub.views


urlpatterns = [
    url(r"^login/$", kobo.hub.views.login, name="auth/login"),
    url(r"^krb5login/$", kobo.hub.views.krb5login, name="auth/krb5login"),
    url(r"^logout/$", kobo.hub.views.logout, name="auth/logout"),
]
