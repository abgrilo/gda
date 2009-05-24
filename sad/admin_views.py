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
    return render_to_response('admin/pick_respostas_modelo.html', {
        } )

# only staff will be able to view this views
pick_respostas = staff_member_required(pick_respostas)
pick_respostas_modelo = staff_member_required(pick_respostas_modelo)
