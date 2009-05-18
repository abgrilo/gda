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
    for d in models.Disciplina.objects.all():
        # pegando atribuiçoes com professores distintos
        for a in models.Atribuicao.objects.filter(disciplina=d).order_by('professor'):
            if not ultima_atribuicao:
                ultima_atribuicao = a
            resps += len(models.Resposta.objects.filter(atribuicao=a))
            # pegando apenas atribuicoes com respostas
            if ultima_atribuicao.professor != a.professor and resps and a.professor != 'não cadastrado no sistema':
                elegiveis.append({'atribuicao' : ultima_atribuicao, 'num' : resps})
                ultima_atribuicao = a
                resps = 0
    return render_to_response('admin/pick_respostas.html', {
        'atrib': elegiveis,
        'ano' : '2008',
        'semestre' : '2'
        } )

def pick_respostas_modelo(request, ano, semestre, disciplina, turma):
    return render_to_response('admin/pick_respostas_modelo.html', {
        } )

# only staff will be able to view this views
pick_respostas = staff_member_required(pick_respostas)
pick_respostas_modelo = staff_member_required(pick_respostas_modelo)
