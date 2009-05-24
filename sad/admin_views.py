#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from sad import models

def pick_respostas(request):
    elegiveis = []
    ultima_atribuicao = None
    resps = 0
    resps_modelo = False
    for d in models.Disciplina.objects.all():
        # pegando atribuiçoes com professores distintos
        for a in models.Atribuicao.objects.filter(disciplina=d).order_by('professor'):
            if not ultima_atribuicao:
                ultima_atribuicao = a
            # computando os dados da última disciplina com o mesmo professor
            if ultima_atribuicao.professor != a.professor:
                if resps:  # apenas coloca na interface as que tem respostas
                    elegiveis.append({'atribuicao' : ultima_atribuicao, 'num' : resps, 'modelo' : resps_modelo})
                ultima_atribuicao = a
                resps = 0
                resps_modelo = False

            # contabilizando respostas dissertativas apenas
            resps += len([r for r in models.Resposta.objects.filter(atribuicao=a) if r.texto])

            if not resps_modelo:  # se houve alguma em uma atribuicao com o mesmo professor, nao recompute
                resps_modelo = bool(models.Resposta.objects.filter(atribuicao=a, modelo=True))
    return render_to_response('admin/pick_respostas.html', {
        'atrib': elegiveis,
        'ano' : '2008',
        'semestre' : '2'
        } )

def pick_respostas_modelo(request, ano, semestre, disciplina, turma):
    u"""Escolher as respostas modelos de uma disciplina+professor.
    Estamos analisando todos os textos (as alternativas podem ter textos também)"""
    d = models.Disciplina.objects.filter(sigla=disciplina)[0]
    p = models.Atribuicao.objects.filter(disciplina=d, turma=turma, semestre=dbSemester(semestre,ano))[0].professor
    atrib = models.Atribuicao.objects.filter(disciplina=d, professor=p, semestre=dbSemester(semestre,ano))

    form = []
    pergs = models.Pergunta.objects.filter(questionario=d.questionario)
    for p in pergs:
        for a in atrib:
            r = models.Resposta.objects.filter(atribuicao=a, pergunta=p)
            resps = [{'id' : resp.id, 'texto' : resp.texto, 'modelo' : resp.modelo} for resp in r if resp.texto]
            if resps:
                form.append({'perg' : p.texto, 'resps' : resps})
        
    return render_to_response('admin/pick_respostas_modelo.html', {
        'disc' : disciplina,
        'professor' : a.professor.nome,
        'data' : form,
        } )

def pick_respostas_modelo_commit(request, ano, semestre, disciplina, turma):
    if request.POST:  # se houver respostas
        for resp in sorted(request.POST):
            r_id = resp.replace('id','')
            r = models.Resposta.objects.filter(id=int(r_id))[0]
            r.modelo = bool(request.POST[resp])
            r.save()
    else:
        return render_to_response('sad/consistency_error.html', {} )

    d = models.Disciplina.objects.filter(sigla=disciplina)[0]
    a = models.Atribuicao.objects.filter(disciplina=d, turma=turma, semestre=dbSemester(semestre,ano))[0]
    return render_to_response('admin/pick_respostas_modelo_commit.html', {
        'disc' : disciplina,
        'professor' : a.professor.nome,
        } )

# only staff will be able to view this views
pick_respostas = staff_member_required(pick_respostas)
pick_respostas_modelo = staff_member_required(pick_respostas_modelo)
pick_respostas_modelo_commit = staff_member_required(pick_respostas_modelo_commit)
