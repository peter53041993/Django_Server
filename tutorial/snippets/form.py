from collections import defaultdict
from random import choices
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
        # ('dev02', 'dev02一般版'), 一般版已經結束運作
        ('fh82dev02', 'dev02合營版'),
        # ('joy188', 'joy188一般版'), 一般版已經結束運作
        ('joy188.teny2020', 'joy188合營版'),
    )
    env = forms.ChoiceField(label='Env', choices=env_choice)
    user = forms.CharField(label='Username', max_length=20, min_length=2)
    nums = forms.IntegerField(label='Quantity', max_value=10000, min_value=1,)
    subtitle = forms.CharField(label='User Header', max_length=11, min_length=2,)
    status_choice = (
        ('one', 'One Layer'),
        ('chain', 'As User Chain')
    )
    status = forms.ChoiceField(label='Type', choices=status_choice,)

class QuickCreateUserForm(forms.Form):
    env_choice = (
        # ('dev02', 'dev02一般版'), 一般版已經結束運作
        ('fh82dev02', 'dev02合營版'),
        # ('joy188', 'joy188一般版'), 一般版已經結束運作
        ('joy188.teny2020', 'joy188合營版'),
    )
    env = forms.ChoiceField(label='Env', choices=env_choice)
    user = forms.CharField(label='Username', max_length=20, min_length=2)
    lower_nums = forms.IntegerField(label='Lowers', max_value=50, min_value=1,)
    layer_nums = forms.IntegerField(label='Layers', max_value=50, min_value=0,)
    subtitle = forms.CharField(label='User Header', max_length=11, min_length=2,)

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


class DatePickerInput(forms.DateInput):
        input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'



class AgentVerifyForm(forms.Form):
    env_choice = (
        (0, 'Dev02'),
        (1, 'Joy188'),
        )

    mode_choice = (
        (0, '團隊'), 
        (1, '個人'),
        )

    env = forms.ChoiceField(label='', choices=env_choice)
    user = forms.CharField(label='用戶名', max_length=16, min_length=4, required=True)
    mode = forms.ChoiceField(label='', choices=mode_choice)
    start_day = forms.DateField(widget=DatePickerInput, label='Start')
    start_time = forms.TimeField(widget=TimePickerInput, label='')
    end_day = forms.DateField(widget=DatePickerInput, label='End')
    end_time = forms.TimeField(widget=TimePickerInput, label='')

class AgentVerifyDetailForm(forms.Form):
    env_choice = (
        (0, 'Dev02'),
        (1, 'Joy188'),
        )
    
    mode_choice = (
        (0, '團隊'), 
        (1, '個人'),
        )
    
    col_choice = (
            (0, '彩票投注'),
            (1, '彩票中獎'),
            (2, '活動'),
            (3, '三方活動'),
            (4, '充值'),
            (5, '提現'),
            (6, '返點'),
            (7, '彩票日工資'),
            (8, '三方返點')
        )

    env = forms.ChoiceField(label='', choices=env_choice)
    user = forms.CharField(label='用戶名', max_length=16, min_length=4, required=True)
    mode = forms.ChoiceField(label='', choices=mode_choice)
    col = forms.ChoiceField(label='', choices=col_choice)
    start_day = forms.DateField(widget=DatePickerInput, label='Start')
    start_time = forms.TimeField(widget=TimePickerInput, label='')
    end_day = forms.DateField(widget=DatePickerInput, label='End')
    end_time = forms.TimeField(widget=TimePickerInput, label='')

class AutoWithdrawVerifyForm(forms.Form):
    env_choice = (
        (0, 'Dev02'),
        (1, 'Joy188'),
        )
    
    env = forms.ChoiceField(label='', choices=env_choice)
    orderID = forms.CharField(label='訂單號', max_length=30, min_length=4, required=True)

#class AddReasonForm(forms.Form):

# Creat your Form wtih ModelForm
# You must to have a model in models.py, like: from .models import some_model
from .models import Snippet
class TestModelFrom(ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'user', 'code', 'linenos', 'language', 'style', 'highlighted']




