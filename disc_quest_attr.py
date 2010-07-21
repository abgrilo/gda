#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

teoricas = [
  'MC009',
  'MC039',
  'MC348',
  'MC426', 
  'MC448', 
  'MC522', 
  'MC526', 
  'MC668', 
  'MC704', 
  'MC714',
  'MC722', 
  'MC822', 
  'MC878', 
  'MC889', 
  'MC898', 
  'MC910',
  'MC920',  
  'MC938',
  'MC948', 
  'MC998', 
  'MO405', 
  'MO417', 
  'MO422', 
  'MO441', 
  'MO637', 
]

praticas = [ 
  'MC011',
  'MC427', 
  'MC613',
  'MC715', 
  'MC723',
  'MC747',
  'MC823',
]

teoricas_praticas = [
  'MC001',
  'MC102', 
  'MC202', 
  'MC326', 
  'MC336', 
  'MC404', 
  'MC436', 
  'MC514', 
  'MC536', 
  'MC542', 
  'MC548', 
  'MC636', 
  'MC750', 
  'MC906',
  'MC942',  
  'MC930', 
  'MO640', 
]

estagio = [
  'MC019', 
  'MC030', 
  'MC032', 
  'MC040', 
  'MC041', 
  'MC050', 
  'MO669', 
  'MO800', 
]

topicos = [
  'MO805', 
  'MO806', 
  'MO809', 
  'MO815', 
  'MO818', 
  'MO825', 
  'MO827', 
  'MO829',
  'MC908', 
  'MC914', 
  'MC918', 
  'MC919',
  'MC926', 
  'MC953',
  'MC956', 
  'MC964', 
  'MC976', 
]

teoricas.extend([
#No lo se - Grad
  'MC852', 
  'MC923', 
  'MC940', 
  'MC950', 
  'MC962', 
#No lo se - PosGrad
  'MO409', 
  'MO410', 
  'MO416', 
  'MO445', 
  'MO601', 
  'MO603', 
  'MO645', 
  'MO648', 
  'MO649', 
  'MO650', 
  'MO901', 
])

def main():
  from sad.models import Disciplina, Questionario

  # montando um dicionário das matérias com o tipo de questionário delas
  discs = {}
  for tipo in ('teoricas', 'praticas', 'teoricas_praticas', 'estagio', 'topicos'):
    for sigla in eval(tipo): # pega a lista com o nome da string
      discs[sigla] = tipo  # e.g discs['MC102'] = 'teorico_praticas'
  
  # adiciona o questionário correto para todas as matérias
  for sigla in discs:
    print 'Incluindo a disciplina %s no questionario %s' % (sigla, discs[sigla])
    try:
      d = Disciplina.objects.filter(sigla=sigla)[0]
    except:
      d = Disciplina(sigla=sigla)
    try:
      q = Questionario.objects.filter(tipo=discs[sigla])[0]
    except:
      # no existe esto questionario!!!
      q = Questionario(tipo=discs[sigla], texto=discs[sigla], semestre='2008-08-01')
      q.save()
    d.questionario = q
    d.save()

  # done!

if __name__ == "__main__":
  main()

