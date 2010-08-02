# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from resultados.views import *


urlpatterns = patterns('resultados.views',
    (r'^$', 'index'),
    (r'^busca', 'busca'),
    (r'^listando/$', 'listing'),
)
