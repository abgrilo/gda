# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from sad.models import *

"""
    Views para consulta das respostas das avaliações.
"""

@login_required(redirect_field_name='redirect_to')
def index(request):
    semestres = Avaliacao.objects.all().order_by()
    return render_to_response('resultados/busca.html', {'semestre': semestres})


@login_required
def busca(request):
    """
        Faz uma busca generica/específica.
    """
    g = request.GET
    if g: # Vai pra página com as respostas da disciplina
        HttpResponseRedirect(disciplina(request))
    p = request.POST
    # dicionário para fazer a busca
    parametros = {}.fromkeys(['semestre', 'disciplina', 'turma', 'professor'])
    for k, v in p.items():
        parametros[k] = v
    
    # filtra os resultados por parâmetros
    atribuicao = Atribuicao.objects.all()
    professor = Professor.objects.all()
    if parametros['semestre']:
        atribuicao = atribuicao.filter(semestre__icontains=parametros['semestre'])
    if parametros['disciplina']:
        atribuicao = atribuicao.filter(disciplina=parametros['disciplina'])
    if parametros['turma']:
        atribuicao = atribuicao.filter(turma__icontains=parametros['turma'])
    if parametros['professor']:
        atribuicao = atribuicao.filter(professor__nome__icontains=parametros['professor'])
    semestre = Avaliacao.objects.all().order_by()
    return render_to_response('resultados/busca.html', {'atribuicao': atribuicao, 'semestre': semestre})


def disciplina(request):
    """
        Mostra as respostas de uma disciplina avaliada. 
    """
    atribuicao = Atribuicao.objects.get(id=request.GET['atribuicao'])
    ano = atribuicao.semestre
    turma = atribuicao.turma
    disciplina = atribuicao.disciplina
    semestre = ano
    professor = atribuicao.professor 
    discs = Disciplina.objects.get(sigla=disciplina)
    try: 
        d = discs
        perguntas = Pergunta.objects.filter(questionario=d.questionario)
        pergL = []
        respL = []
        atribuicao = Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, semestre=semestre)

        for pergunta in perguntas:
            respostas = Resposta.objects.filter(pergunta=pergunta, atribuicao=atribuicao)
            if not respostas:
                respL.append('')
            elif pergunta.tipo == 'A':  # alternativa
                respL.append(respostas[0].alternativa)
            else:    
                respL.append(respostas[0].texto)
            if pergunta.tipo == 'A':  # alternativa 
                alters = Alternativa.objects.filter(pergunta=pergunta)
                alterL = []
                respL = []
                for a in alters:
                    r = respostas.filter(alternativa=a.id)
                    respL.append({'id': a.id, 'quantidade': r.count()})
                    alterL.append({'id' : a.id, 'texto' : a.texto, 'resposta': r.count()})
                pergL.append({'id' : pergunta.id, 'pergunta' : pergunta.texto, 'alternativas' : alterL,})
            else:
                respL = []
                for r in respostas:
                    print r
                    if r.texto is not None:
                        respL.append({'id' : pergunta.id, 'resposta' : r.texto, })
                pergL.append({'id' : pergunta.id, 'pergunta' : pergunta.texto, 'dissertativas' : respL,})
        return render_to_response('resultados/respostas.html',
                                  { 'semestre': semestre ,
                                    'disciplina': disciplina,
                                    'professor': professor,
                                    'turma': turma,
                                    'perguntas': pergL,
                                    } 
                                  )
    except:
        return render_to_response('sad/consistency_error.html', {} )
