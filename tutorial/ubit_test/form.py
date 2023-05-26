from collections import defaultdict
from random import choices
from django import forms
from django.forms import fields
from django.forms.models import ModelForm

class UbitTrunkForm(forms.Form):
    choices_feild =(
        (0, 'Ubit DEV'),
        (1, 'Ubit STG'),
        )
    env = forms.ChoiceField(label='Env', choices=choices_feild, 
                            help_text='自動化結果需要約3分鐘，請勿關閉視窗')
