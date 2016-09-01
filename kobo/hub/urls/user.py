# -*- coding: utf-8 -*-


from django.contrib.auth import get_user_model
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from kobo.django.views.generic import ExtraListView
from kobo.hub.views import UserDetailView


urlpatterns = [
    url(r"^$", ExtraListView.as_view(
        queryset=get_user_model().objects.order_by("username"),
        template_name="user/list.html",
        context_object_name="usr_list",
        title = _('Users'),
    ), name="user/list"),
    url(r"^(?P<pk>\d+)/$", UserDetailView.as_view(), name="user/detail"),
]
