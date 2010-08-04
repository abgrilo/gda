
from django.conf.urls.defaults import *

from views import index, busca, disciplina

urlpatterns = patterns('resultados.views',
    (r'^$', 'index'),
    (r'^respostas/$', 'disciplina'),
    (r'^lista/disciplinas/$', 'busca'),
)
