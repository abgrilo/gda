# -*- coding: utf-8 -*-
from sad.models import *
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


class QuestionarioInline(admin.TabularInline):
    model = Questionario

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'semestre', 'data_inicio', 'data_fim', 
                    'liberar_consultas']
    search_fields = ['nome']
    ordering = ['-ano', '-semestre']
    inlines = [QuestionarioInline]
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        """ 
            Determina o HttpResponse para add_avaliacao. 
            Este código é uma personalização de um trecho de código do django
            /django/contrib/admin/options.py 
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Avaliação adicionada com sucesso."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect(reverse("admin:sad_avaliacao_changelist"))
       

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ['nome']
    ordering = ['nome']

class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'texto')
    list_filter = ['tipo']
    search_fields = ('texto',)

class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nome']
    ordering = ['nome']

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('username','nome','email', 'curso',)
    list_filter = ['curso']
    search_fields = ['username', 'nome', 'email']
    ordering = ['username']

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    search_fields = ['sigla', 'nome']
    ordering = ['sigla']

class AtribuicaoAdmin(admin.ModelAdmin):
    list_display = ('disciplina','professor', 'turma')
    list_filter = ['disciplina', 'professor']
    search_fields = ['disciplina'] 
    ordering = ['disciplina']    

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados', {'fields': ['tipo', 'questionario',]},),
        ('Pergunta', {'fields': ['texto',]},),
        ]
    search_fields = ['texto']
    list_display = ('texto', 'tipo',)
    list_filter = ['tipo', 'questionario']

class RespostaAdmin(admin.ModelAdmin):
    def textoOuAlternativa(obj):
        resposta = obj.alternativa if obj.alternativa else obj.texto
        return resposta if resposta else " --- Sem resposta --- " 
    textoOuAlternativa.short_description = 'Resposta'

    list_display = ('pergunta', textoOuAlternativa, 'atribuicao',)
    list_filter = ['atribuicao',]
     
    
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pergunta',)
    list_filter = ['pergunta',]
    search_fields = ['texto']
    ordering = ['pergunta']

#class GenreAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#
#class MovieAdmin(admin.ModelAdmin):
#    fieldsets = [('General Info',      {'fields': ['title','title_br','pub_date', 'imdb']}),
#                 ('Plot',    {'fields': ['plot'], 'classes': ['collapse']}),
#                 ('Crew',    {'fields': ['cast', 'director']}),
#                 ('Genres',  {'fields': ['genres']}),
#                 ('Quality', {'fields': ['height', 'width']}),
#                 ('Path',    {'fields': ['path', 'owner']}),
#                 ]
#    list_display = ('title', 'title_br', 'year',)
#    list_filter = ['pub_date',]
#    search_fields = ['title', 'title_br']
#    date_hierarchy = 'pub_date'


#admin.site.register(Curso, CursoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Atribuicao, AtribuicaoAdmin)
admin.site.register(Questionario, QuestionarioAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
