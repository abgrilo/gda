#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from sad import models
from gdadefs import *
from md5 import new

# FIXME: Arrumar estas variaveis globais
ANO, SEMESTRE = '2010', '1'

def show_all_semesters(request):
    semesters = ["Bla", "Creu", "GDA"]
    return render_to_response('sad/all_semesters.html', { 'semesters': semesters} )

def show_all_courses(request, ano, semestre):
    return render_to_response('sad/all_courses.html', { 'ano': ano , 'semestre': semestre } )

def view_result(request):
  professores = models.Professor.objects.all()
  disciplinas = models.Disciplina.objects.all()
  return render_to_response('sad/view_result.html', { 'professores': professores , 'disciplinas': disciplinas } )

def format_respostas(respostas):
  result = []
  anterior = None
  for r in respostas:
    if anterior == None or anterior.pergunta.id != r.pergunta.id:
      atual = []
      result.append(atual)
      atual.append(r.pergunta.texto)
      respostas = []
      atual.append(respostas)
    anterior = r
    if r.pergunta.tipo == 'A':
      if r.alternativa:
        respostas.append(r.alternativa.texto)
    else:
      if r.texto:
        respostas.append(r.texto)

  return result

def query_result(request):
  professores = models.Professor.objects.all()
  disciplinas = models.Disciplina.objects.all()
  if request.POST:
      professor = request.POST['professores']
      disciplina = request.POST['disciplinas']
      if professor and disciplina:
        respostas = models.Resposta.objects.filter(atribuicao__disciplina__sigla=disciplina, atribuicao__professor__id=professor).order_by('pergunta__id')
        result = format_respostas(respostas)
        return render_to_response('sad/view_result.html', { 'professores': professores , 'disciplinas': disciplinas, 'respostas': result} )
  return render_to_response('sad/view_result.html', { 'professores': professores , 'disciplinas': disciplinas } )


def respostas_alternativas(request):
    professores = models.Professor.objects.all()
    disciplinas = models.Disciplina.objects.all()
    return render_to_response('sad/respostas_alternativas.html',
            { 'professores': professores , 
              'disciplinas': disciplinas })

def format_respostas_alternativas(respostas):
    result = []
    anterior = respostas[0]
    alternativas = {}
    
    for r in respostas:
        if anterior.pergunta.id != r.pergunta.id:
            atual = []
            result.append(atual)
            atual.append(r.pergunta.texto)
            respostas = []
            for i in alternativas:
                alternativa = i+':  '+ str(alternativas[i])
                respostas.append(alternativa)
            alternativas = {}
            atual.append(respostas)
        anterior = r
        if r.alternativa:
            if r.alternativa.texto in alternativas:
                alternativas[r.alternativa.texto] += 1
            else: 
                alternativas[r.alternativa.texto] = 1
    return result                

def query_alternativas(request):
  professores = models.Professor.objects.all()
  disciplinas = models.Disciplina.objects.all()
  if request.POST:
      professor = request.POST['professores']
      disciplina = request.POST['disciplinas']
      if professor and disciplina:
        respostas = models.Resposta.objects.filter(
                        atribuicao__disciplina__sigla=disciplina
                    ).filter(
                        atribuicao__professor__id=professor
                    ).order_by(
                        'pergunta__id'
                    )
        result = format_respostas_alternativas(respostas)
        return render_to_response(
                'sad/respostas_alternativas.html', 
                { 'professores': professores , 
                  'disciplinas': disciplinas, 
                  'respostas': result } )
  return render_to_response('sad/respostas_alternativas.html', 
        { 'professores': professores , 
          'disciplinas': disciplinas } )


def show_all_answers(request, ano, semestre,disciplina):
    answers = ["Foi phoda!", "coxa!"]
    return render_to_response('sad/all_answers.html', 
                              { 'ano': ano , 
                                'semestre': semestre , 
                                'answers': answers ,
                                } 
                              )

def all_to_answer(request, ano, semestre, respondido = False, ultima_resp = ''):
    if request.user.is_authenticated():
        try:
            # procura o objeto aluno
            aluno = models.Aluno.objects.filter(username=request.user.username)[0]
            # pega as disciplinas desse semestre
            atribuicaoPadrao = models.Atribuicao.objects.filter(aluno=aluno, semestre=dbSemester(semestre, ano))
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
        return render_to_response('sad/all_to_answer.html', 
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'atribuicao': atribuicao,
                                    'atr_resp': atr_resp,
                                    'respondido': respondido,
                                    'ultima_resp' : ultima_resp,
                                    }
                                  )
    else:
        return render_to_response('sad/home.html',  {'logado': 0} )

def answer_course(request, ano, semestre, disciplina, turma):
    discs = models.Disciplina.objects.filter(sigla=disciplina)
    try:
        aluno = models.Aluno.objects.filter(username=request.user.username)[0]
        d = discs[0]  # sera lidado uma disciplina por vez no questionario
        pergs = models.Pergunta.objects.filter(questionario=d.questionario)
        pergL = []
        respL = []
        hash = new(request.user.username).hexdigest()
        atr = models.Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, semestre=dbSemester(semestre,ano), aluno=aluno)[0]
        if models.Resposta.objects.filter(hash_aluno=hash, atribuicao=atr):
            return render_to_response('sad/consistency_error.html', {} )

        for p in pergs:
            r = models.Resposta.objects.filter(pergunta=p, hash_aluno=hash, atribuicao=atr)
            if not r:
                respL.append('')
            elif p.tipo == 'A':  # alternativa
                respL.append(r[0].alternativa)
            else:    
                respL.append(r[0].texto)

            if p.tipo == 'A':  # alternativa 
                alters = models.Alternativa.objects.filter(pergunta=p)
                alterL = []
                for a in alters:
                    alterL.append({'id' : a.id, 'texto' : a.texto,})
                pergL.append({'id' : p.id, 'pergunta' : p.texto, 'alternativas' : alterL,})
            else:
                pergL.append({'id' : p.id, 'pergunta' : p.texto, })

        return render_to_response('sad/answer_course.html',
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'disciplina': disciplina,
                                    'turma': turma,
                                    'perguntas': pergL,
                                    'respostas': respL,
                                    'nome': d.nome,
                                    'atribuicao' : atr,
                                    } 
                                  )
    except:
        return render_to_response('sad/consistency_error.html', {} )

def commit_answer_course(request, ano, semestre, disciplina, turma):
    if request.GET:  # se houver respostas
        atribuicao = models.Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, semestre=dbSemester(semestre,ano))[0]
        hash = new(request.user.username).hexdigest()
        if models.Resposta.objects.filter(hash_aluno=hash, atribuicao=atribuicao):
          return render_to_response('sad/error.html', {'error': 'A avaliação do professor já foi enviada anteriormente'} )
        for resp in sorted(request.GET):
            if resp.startswith('pa'):  # alternativas
                p_id = resp.replace('pa','')
                # FIXME gambiarra pra interface admin
                # se o texto não existir a interface capota.
                text = '' 
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                alter = models.Alternativa.objects.filter(id=request.GET[resp])[0]
                r = models.Resposta.objects.filter(pergunta=perg, 
                        hash_aluno=hash, 
                        atribuicao=atribuicao)
                if not r:
                    r = models.Resposta(pergunta=perg, 
                            texto=text, alternativa=alter, 
                            hash_aluno=hash, atribuicao=atribuicao)
                    r.save()
            else:  # dissertativa
                p_id = resp.replace('pd','')
                text = request.GET[resp]
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                r = models.Resposta.objects.filter(pergunta = perg, 
                        atribuicao=atribuicao, hash_aluno = hash)
                if r:
                    r = r[0]
                    r.texto = text
                    r.save()  
                else:
                    alter = None
                    r = models.Resposta(pergunta=perg, texto=text, alternativa=alter, 
                            hash_aluno=hash, atribuicao=atribuicao)
                    r.save()
        return all_to_answer(request, ano, semestre, True, disciplina+turma)
    else:
        return render_to_response('sad/consistency_error.html', {} )

def home(request):
    if request.user.is_authenticated():
        # proceed if already authenticated
        return all_to_answer(request, ANO, SEMESTRE) 
    else:
        return render_to_response('sad/home.html', {'error' : False,})
        

def login_auth(request, a):
    try:
        #if request.user.is_
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            #FIXME gambiarra
            return all_to_answer(request, ANO, SEMESTRE)
        else:
            # Show same error as an exception
            raise
    except:
        return render_to_response('sad/home.html', {'error' : True,})

def logout(request):
    auth.logout(request)
    return home(request)


