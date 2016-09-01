# -*- coding: utf-8 -*-


from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from kobo.django.views.generic import ExtraListView
from kobo.hub.views import ArchDetailView
from kobo.hub.models import Arch


urlpatterns = [
    url(r"^$", ExtraListView.as_view(
        queryset=Arch.objects.order_by("name"),
        template_name="arch/list.html",
        context_object_name="arch_list",
        title=_("Architectures"),
    ), name="arch/list"),
    url(r"^(?P<pk>\d+)/$", ArchDetailView.as_view(), name="arch/detail"),
]
