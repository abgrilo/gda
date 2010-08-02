# -*- encoding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q

from sad.models import *
from resultados.forms import *


"""
    Views para consulta das respostas das avaliações.
"""


def index(request):
    """
        XXX: quando terminar de desenvolver/testar, requerer login.
        dummy page
    """
    return render_to_response('resultados/busca.html')

    if request.POST:
        semestre = request.POST['semestres']
        professor = request.POST['professores']
        disciplina = request.POST['disciplinas']
    return HttpResponse('<html><body> Dummy, FIXME!</body></html>')

def listing(request):
    """ 
        Lista os professores cadastrados.
        XXX: Colocar links para as matérias lecionadas pelo professor.
        XXX: listar por instituto quando esta tabela estiver no GDA.
    """
    professores_list = Professor.objects.order_by('nome')
    paginator = Paginator(professores_list, 50, orphans=5)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        professores = paginator.page(page)
    except (EmptyPage, InvalidPage):
        professores = paginator.page(paginator.num_pages)

    return render_to_response('resultados/list.html', {
            "professores": professores})


def busca(request):
    """
        Faz uma busca genericao.
    """
    #return HttpResponse('<html><h1>Olá avaliação genérica</h1></html>')
    #return disciplina(ano, semestre, disciplina, turma)
    return disciplina('2010', '2010-01-01', 'MC548', 'A')

def disciplina(ano, semestre, disciplina, turma):
    """
        Mostra as respostas de uma disciplina avaliada. 
    """
    discs = Disciplina.objects.get(sigla=disciplina)
    #try: FIXME só pra debug
    if True:
        d = discs
        perguntas = Pergunta.objects.filter(questionario=d.questionario)
        #print perguntas[0].id
        pergL = []
        respL = []
        atribuicao = Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, semestre=semestre)

        for pergunta in perguntas:
            respostas = Resposta.objects.filter(pergunta=pergunta, atribuicao=atribuicao)
            #print respostas[0].alternativa, respostas[1].alternativa, respostas[3].alternativa
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
                    if r.texto is not None:
                        respL.append({'id' : pergunta.id, 'resposta' : r.texto, })
                pergL.append({'id' : pergunta.id, 'pergunta' : pergunta.texto, 'dissertativas' : respL,})
        
        return render_to_response('resultados/respostas.html',
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'disciplina': disciplina,
                                    'turma': turma,
                                    'perguntas': pergL,
                                    } 
                                  )
    #except:
    #    return render_to_response('sad/consistency_error.html', {} )
