# -*- coding: utf-8 -*-

from django import forms


class BuscaForm(forms.Form):
    semestre = forms.DateField() # FIXME mostrar opções de semestre
    professor = forms.CharField(required=False)
    disciplina = forms.CharField(max_length=6)
    turma = forms.CharField(max_length=1)

        


