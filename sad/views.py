#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from sad import models
from gdadefs import *
from md5 import new
from django.db.models import F

@login_required
def show_all_semesters(request):
    semesters = ["Bla", "Creu", "GDA"]
    return render_to_response('sad/all_semesters.html', { 'semesters': semesters} )

@login_required
def show_all_courses(request, ano, semestre):
    return render_to_response('sad/all_courses.html', { 'ano': ano , 'semestre': semestre } )

@login_required
def show_all_answers(request, ano, semestre,disciplina):
    answers = ["Foi phoda!", "coxa!"]
    return render_to_response('sad/all_answers.html', 
                              { 'ano': ano , 
                                'semestre': semestre , 
                                'answers': answers ,
                                } 
                              )
@login_required
def all_to_answer(request, ano, semestre, respondido = False, ultima_resp = ''):
    avaliacao = models.Avaliacao.objects.get(ano=ano, semestre=semestre)
    try:
        # procura o objeto aluno
        aluno = models.Aluno.objects.filter(username=request.user.username)[0]
        # pega as disciplinas desse semestre
        atribuicaoPadrao = models.Atribuicao.objects.filter(aluno=aluno, avaliacao=avaliacao)
        # mostra apenas as disciplinas que ele ainda nao respondeu
        hash = new(request.user.username).hexdigest()
        atribuicao = []
        atr_resp = []
        for atr in atribuicaoPadrao:
            # FIXME deveria ser mais limpo, um if
            if not models.Resposta.objects.filter(hash_aluno=hash, atribuicao=atr):
                # remove a atribuicao ja respondida 
                atribuicao.append(atr)
            else:
                atr_resp.append(atr)
    except:
    # provavelmente o aluno nao esta fazendo nenhuma discplina
        atribuicao = []
        atr_resp = []
    return render_to_response(
        'sad/all_to_answer.html', { 
            'ano': ano,
            'semestre': semestre,
            'atribuicao': atribuicao,
            'atr_resp': atr_resp,
            'respondido': respondido,
            'ultima_resp' : ultima_resp,
         }
    )


@login_required
def answer_course(request, ano, semestre, disciplina, turma):
    discs = models.Disciplina.objects.filter(sigla=disciplina)
    try:
        avaliacao = models.Avaliacao.objects.get(ano=ano, semestre=semestre)
        aluno = models.Aluno.objects.filter(username=request.user.username)[0]
        d = discs[0]  # sera lidado uma disciplina por vez no questionario
        pergs = models.Pergunta.objects.filter(questionario=d.questionario)
        pergL = []
        respL = []
        hash = new(request.user.username).hexdigest()
        atr = models.Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, avaliacao=avaliacao, aluno=aluno)[0]
        for p in pergs:
            try:
                r = models.Resposta.objects.get(pergunta=p, hash_aluno=hash, atribuicao=atr)
            except:
                r = None
            if p.tipo == 'A':  # alternativa 
                alters = models.Alternativa.objects.filter(pergunta=p)
                alterL = []
                for a in alters:
                    if r:
                        comentario = r.texto
                        if r.alternativa is not None and r.alternativa.id == a.id:
                            checked = 'checked' 
                        else:
                            checked = ''
                    else:
                        comentario = ''
                        checked = ''
                    alterL.append({'id': a.id, 'texto': a.texto, 'checked': checked})
                pergL.append({
                    'id': p.id, 
                    'pergunta': p.texto, 
                    'alternativas': alterL, 
                    'texto': comentario,
                })
            else:
                if r:
                    texto = r.texto
                else:
                    texto = ''
                pergL.append({'id' : p.id, 'pergunta' : p.texto, 'texto': texto })
        return render_to_response('sad/answer_course.html',
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'disciplina': disciplina,
                                    'turma': turma,
                                    'perguntas': pergL,
                                    'nome': d.nome,
                                    'atribuicao' : atr,
                                    } 
                                  )
    except:
        return render_to_response('sad/consistency_error.html', {} )

@login_required
def commit_answer_course(request, ano, semestre, disciplina, turma):
    if request.GET:  # se houver respostas
        avaliacao = models.Avaliacao.objects.get(ano=ano, semestre=semestre)
        atribuicao = models.Atribuicao.objects.get(
            avaliacao=avaliacao,
            disciplina=disciplina,
            turma=turma)
        hash = new(request.user.username).hexdigest()
        for resp in sorted(request.GET):
            if resp.startswith('pa'):  # alternativas
                p_id = resp.replace('pa','')
                # FIXME gambiarra pra interface admin
                # se o texto não existir a interface capota.
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                alter = models.Alternativa.objects.filter(id=request.GET[resp])[0]
                texto = ''
                try:
                    r = models.Resposta.objects.get(
                        pergunta=perg, 
                        hash_aluno=hash, 
                        atribuicao=atribuicao
                    )
                    r.alternativa = alter
                    r.texto = texto
                except:
                    r = models.Resposta(
                        pergunta=perg, 
                        texto=texto, 
                        alternativa=alter, 
                        hash_aluno=hash, 
                        atribuicao=atribuicao
                    )
                r.save()
            else:  # dissertativa
                p_id = resp.replace('pd','')
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                texto = request.GET[resp]
                try:
                    r = models.Resposta.objects.get(
                        pergunta = perg, 
                        atribuicao=atribuicao, 
                        hash_aluno = hash
                    )
                    r.texto = texto
                except:
                    alter = None
                    r = models.Resposta(pergunta=perg, texto=texto, alternativa=alter, 
                            hash_aluno=hash, atribuicao=atribuicao)
                r.save()
        return all_to_answer(request, ano, semestre, True, disciplina+turma)
    else:
        return render_to_response('sad/consistency_error.html', {} )

def home(request):
    if request.user.is_authenticated():
        # proceed if already authenticated
        avaliacao = models.Avaliacao.objects.get(ano='2010', semestre='2')
        return all_to_answer(request, avaliacao.ano, avaliacao.semestre) 
    else:
        return render_to_response('sad/home.html', {'error' : False,})
        
def logout(request):
    auth.logout(request)
    return home(request)
    #XXX redirecionar para uma tela informando que foi realizado o logout


