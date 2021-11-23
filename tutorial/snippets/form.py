from collections import defaultdict
from django import forms
from django.forms import fields
from django.forms.models import ModelForm

import django_tables2 as tables 

class TestForm(forms.Form):
    #test_value = forms.CharField(label='test_value',)
    
    choices_feild =(
        (0, 'dev02'),
        (1, 'joy188'),
        )
    test_env = forms.ChoiceField(label='Env', choices=choices_feild, help_text='選擇環境')
    
    test_user = forms.CharField(label='Username', max_length=20, min_length=2, help_text='輸入用戶名')

class CreateUserForm(forms.Form):
    env_choice = (
        ('dev02', 'dev02一般版'),
        ('fh82dev02', 'dev02合營版'),
        ('joy188', 'joy188一般版'),
        ('joy188.195353', 'joy188合營版'),
    )
    env = forms.ChoiceField(label='Env', choices=env_choice)
    user = forms.CharField(label='Username', max_length=20, min_length=2)
    nums = forms.IntegerField(label='Quantity', max_value=50, min_value=1,)
    subtitle = forms.CharField(label='User Header', max_length=11, min_length=2,)
    status_choice = (
        ('one', 'One Layer'),
        ('chain', 'As User Chain')
    )
    status = forms.ChoiceField(label='Type', choices=status_choice,)

class CreateUserTable(tables.Table):
    row_number = tables.Column(empty_values=())
    user = tables.Column()
    chain = tables.Column()

class GetAvailableBalanceForm(forms.Form):
    env_choice = (
        (0, 'dev02'),
        (1, 'joy188'),
    )
    env = forms.ChoiceField(label='Env', choices=env_choice)
    
    range_min = forms.IntegerField(label='範圍', min_value=0, required=False)
    range_max = forms.IntegerField(label='-', min_value=0, required=False)
    user = forms.CharField(label='用戶名', max_length=16, min_length=4, required=False)

class Activity531Form(forms.Form):
    type_choice = (
        (0, '昨日排行'),
        (1, '今日即時排行'),
    )
    search_type = forms.ChoiceField(label='搜尋', choices=type_choice)

class FreeIpBlockForm(forms.Form):
    user = forms.CharField(label='用戶')
    ip = forms.CharField(label='本地IP')


#class AddReasonForm(forms.Form):

# Creat your Form wtih ModelForm
# You must to have a model in models.py, like: from .models import some_model
from .models import Snippet
class TestModelFrom(ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'user', 'code', 'linenos', 'language', 'style', 'highlighted']




