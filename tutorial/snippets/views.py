from queue import Empty
import re
#from typing_extensions import get_args
from urllib.parse import urlencode
from django import shortcuts
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response
from rest_framework.decorators import api_view, schema
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



'''
1. function base
'''
@csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

'''
2. class base
'''
from rest_framework.views import APIView
from django.http import Http404

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
3. class base + "mixins"
'''
from rest_framework import mixins
from rest_framework import generics

class SnippetListM(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetailM(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

'''
4. class base + generic class-based views
'''    
class SnippetListG(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]



class SnippetDetailG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


'''
add user Authentication & Permissions
'''
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
Creating an endpoint for the root of API
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
        'test': reverse('test-api', request=request, format=format),
        'trunk_test': reverse('trunk_test', request=request, format=format),
        # 'autoWithdrawVerify': reverse('autoWithdrawVerify', request=request, format=format)
    })

from rest_framework import renderers
from rest_framework.response import Response

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


from .FF_.superdatagenerator import Super2000Data


'''
test: local module in rest-framework
'''
@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
        return Response('Using POST to set your search value')
    elif request.method == 'POST':
        env = request.data['env']
        lotteryid = request.data['lotteryid']
        moneyunit = request.data['moneyunit']
        awardMode = request.data['awardMode']
        return Response(Super2000Data().ballContentAll2000(env, lotteryid, moneyunit, awardMode))

@api_view(['GET' ,'POST'])
def sale_switch(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        env = request.data['env']
        sale = request.data['sale']
        lottery_type = request.data['lottery_type']
        if not lottery_type:
            Super2000Data().saleSwitch(env, sale)
        elif lottery_type:
            Super2000Data().saleSwitch(env, sale, lottery_type)
    return

'''
trunk test
'''

from .FF_.trunk_execute import run_trunk
from django.http import FileResponse


@csrf_exempt
@api_view(['GET'])
def trunk_config(requsest):
    tips = 'set query: 1.web_api, 2.web_front, 3.iapi, 4.all'
    return Response(tips)


@csrf_exempt
@api_view(['GET'])
def trunk_test(request, unittype):

    fp = run_trunk(unittype)
    file = open(f'C:\\Users\\Peter\\drf_test\\tutorial\\snippets\\trunk_reports\\{fp}', 'rb')

    return FileResponse(file)

'''
test Form: using form model
'''
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render

from .form import TestForm
from .form import TestModelFrom
from .form import CreateUserTable


@api_view(['POST', 'GET'])
def test_form(request):
    form = TestModelFrom()
    return render(request, 'test0910.html', {'form': form})

from .form import CreateUserForm
from .FF_.seleniumjob import AutoFrontTools

@api_view(['POST', 'GET'])
def createUser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            env = form.cleaned_data['env']
            user = form.cleaned_data['user']
            nums = form.cleaned_data['nums']
            subtitle = form.cleaned_data['subtitle']
            status = form.cleaned_data['status']

            if env in ['joy188','joy188.teny2020']: 
                envs = 1
            elif env in ['dev02','dev03','fh82dev02']:
                envs = 0
            else:
                envs = 1

            if Super2000Data().selectUserid(envs, user):
                AutoFrontTools().login(env, user)

                res = AutoFrontTools().registerUser(user, nums, subtitle, status)
                res[0].remove(user) # remove original user

                create_list = []
                count = 0
                for new_user in res[0]:
                    user_chain = Super2000Data().getUserChain(envs, new_user)
                    data_ =  [str(count+1), new_user, user_chain]
                    create_list.append(data_)
                    count += 1

                return render(request, 'test_form.html', {
                    'form': form, 
                    'create_list': create_list,
                    'message': res[1],
                    }
                    )
            else:
                error_message = '用戶不存在'
                return  render(request, 'test_form.html', {'form': form, 'error_message': error_message})    
    else:
        form = CreateUserForm()
    
    return render(request, 'test_form.html', {'form': form})

from .form import QuickCreateUserForm
@api_view(['POST', 'GET'])
def quickCreatUser(request):
    
    if request.method == 'POST':
        form = QuickCreateUserForm(request.POST)
        if form.is_valid():
            env = form.cleaned_data['env']
            user = form.cleaned_data['user']
            lower_nums = form.cleaned_data['lower_nums']
            layer_nums = form.cleaned_data['layer_nums']
            subtitle = form.cleaned_data['subtitle']

            if env in ['joy188','joy188.teny2020']: 
                envs = 1
            elif env in ['dev02','dev03','fh82dev02']:
                envs = 0
            else:
                envs = 0

            if Super2000Data().selectUserid(envs, user):
                AutoFrontTools().login(env, user)

                create_list = []
                count = 0
                res = tuple()
                for i in range(lower_nums):
                    res = AutoFrontTools().registerUser(user, layer_nums, subtitle, 'chain')
                    res[0].remove(user) # remove original user
                    
                    for new_user in res[0]:
                        user_chain = Super2000Data().getUserChain(envs, new_user)
                        data_ =  [str(count+1), new_user, user_chain]
                        create_list.append(data_)
                        count += 1

                return render(request, 'quick_creat.html', {
                    'form': form, 
                    'create_list': create_list,
                    'message': res[1],
                    }
                    )
            else:
                error_message = '用戶不存在'
                return  render(request, 'quick_creat.html', {'form': form, 'error_message': error_message})    
    else:
        form = QuickCreateUserForm()
    
    return render(request, 'quick_creat.html', {'form': form})
    


from .form import GetAvailableBalanceForm
@api_view(['POST', 'GET'])
def getAvlBal(request):
    contacts = ''
    error_message =''
    
    if request.method == 'POST':
        form = GetAvailableBalanceForm(request.POST)

        if form.is_valid():
            # 取得資料列表: result_list
            env = int(form.cleaned_data['env'])
            range_max = form.cleaned_data['range_max'] 
            range_min = form.cleaned_data['range_min']
            user = str(form.cleaned_data['user'])

            result_list = []
            
            # 參數存 session, 新請求送出後才覆蓋
            # request.session['env'] = env
            # request.session['range_max'] = range_max if range_max else request.session.get('range_max')
            # request.session['range_min'] = range_min if range_min else request.session.get('range_min')
            # request.session['user'] = user

            # 若沒帶參數，使用session值
            # env = env if env else request.session.get('env')
            # range_max = range_max if range_max else request.session.get('range_max')
            # range_min = range_min if range_min else request.session.get('range_min')
            # user = user if user else request.session.get('user')


            if not user: 
                range_max = int(range_max) if range_max != None else 'infinity'
                range_min = int(range_min) if range_min != None else 0
                res = Super2000Data().getUserAvailableBalance(env, balance_range=(range_min, range_max))
            else:
                if Super2000Data().selectUserid(env, user):
                    res = Super2000Data().getUserAvailableBalance(env, user=user)
                else:
                    error_message = '用戶不存在'
                    res = []

            for data in res:
                res[data][0] = '一般' if res[data][0] ==0 else '合營'
                res[data][1] = '一般' if res[data][0] ==0 else '星級'
                data_ = [data] + [i for i in res[data]]
                result_list.append(data_)
            
            # 分頁器邏輯:
            page = request.GET.get('page')
            paginator = Paginator(result_list, 10)
            

            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # 若非整數，取第一頁
                contacts = paginator.page(1)
            except EmptyPage:
                # 若範圍外，取最後一頁
                contacts = paginator.page(paginator.num_pages)
            
            
            return render(request, 'available_balance_search.html', {
                'form': form,
                'result_list': contacts,
                'error_message': [request.session.get('env'), request.session.get('range_max'), request.session.get('range_min'), request.session.get('user')],
            }
            )          
    else:
        form = GetAvailableBalanceForm()



    return render(request, 'available_balance_search.html',  {
        'form': form,
        }
    )

import datetime
from .form import Activity531Form
@api_view(['POST', 'GET'])
def activity531(request):
    error_message =''
    if request.method == 'POST':
        form = Activity531Form(request.POST)
        

        if form.is_valid():
            search_type = int(form.cleaned_data['search_type'])
            result_list_normal = Super2000Data().activity531Rank(search_type, 0)
            result_list_fh = Super2000Data().activity531Rank(search_type, 1)


            now = datetime.date.today()
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            if search_type == 0:
                time_text = f'{yesterday.year} {yesterday.month}/{yesterday.day} - {now.year} {now.month}/{now.day}'
            elif search_type == 1:
                time_text = f'{now.year} {now.month}/{now.day} - '
            else:
                time_text = None

            return render(request, 'activity531.html', {
                'form': form,
                'result_list_normal': result_list_normal,

                'result_list_fh': result_list_fh,
                'time_text': time_text,
                })
    else:
        form = Activity531Form()

    return render(request, 'activity531.html', {'form': form})  

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip  

from .form import FreeIpBlockForm
from .FF_.tools import ip4ToInt
from .FF_.Connection import RedisConnection
@api_view(['POST', 'GET'])
def freeIpBlock(request):
    error_message =''
    if request.method == 'POST':
        form = FreeIpBlockForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            ip = str(form.cleaned_data['ip'])
            ip_int = ip4ToInt(ip)

            redis_conn = RedisConnection().get_rediskey(0)
            redis_conn.set(f'verifyIp{user}', ip_int)
            #header = request.headers
            #cookies = request.COOKIES
            text = '修改成功'

            return render(request, 'freeIp.html', {'form': form, 'text': text})
    else:
        form = FreeIpBlockForm()
    return render(request, 'freeIp.html', {'form': form})

@api_view(['GET'])
def activity578(request):
    t_range = ('2022-01-12 00:00:00', '2022-01-17 00:00:00')
    rnak_dict = Super2000Data().activity578Rank(t_range[0], t_range[1])
    return JsonResponse(rnak_dict)

from .FF_.make_agent_data import AgentCenter
from .form import AgentVerifyForm
@api_view(['POST', 'GET'])
def agentVerify(request):
    if request.method == 'POST':
        form = AgentVerifyForm(request.POST)


        total_list = []
        fh_list = []
        third_list = []
        if form.is_valid():
            # 取得資料列表: result_list
            env = int(form.cleaned_data['env'])
            user = str(form.cleaned_data['user'])
            mode = int(form.cleaned_data['mode'])
            start = form.cleaned_data['start_day'].strftime("%Y-%m-%d ") + form.cleaned_data['start_time'].strftime("%H:%M:%S")
            end = form.cleaned_data['end_day'].strftime("%Y-%m-%d ") + form.cleaned_data['end_time'].strftime("%H:%M:%S")

            result_dict = AgentCenter().verifyAgentData(env, user, start, end, mode)
            
            
            for k in result_dict['TOTAL']:
                total_list.append(round(result_dict['TOTAL'][k], 4))
            
            
            for k in result_dict['FH']:
                fh_list.append(round(result_dict['FH'][k], 4))
            
            third_list = []
            for k in result_dict['THIRD']:
                third_list.append(round(result_dict['THIRD'][k], 4))
        
        return render(request, 'agentverify.html', {
            'form': form,
            'total_list': total_list,
            'fh_list': fh_list,
            'third_list': third_list,
            })
        # return JsonResponse(result_dict)
    else:
        form = AgentVerifyForm()
        return render(request, 'agentverify.html', {'form': form})


from .form import AgentVerifyDetailForm
@api_view(['POST', 'GET'])
def agentVerifyDetail(request):
    if request.method == 'POST':
        form = AgentVerifyDetailForm(request.POST)

        result = None
        total_value = None
        if form.is_valid():
            # 取得資料列表: result_list
            env = int(form.cleaned_data['env'])
            user = str(form.cleaned_data['user'])
            mode = int(form.cleaned_data['mode'])
            col = int(form.cleaned_data['col'])
            start = form.cleaned_data['start_day'].strftime("%Y-%m-%d ") + form.cleaned_data['start_time'].strftime("%H:%M:%S")
            end = form.cleaned_data['end_day'].strftime("%Y-%m-%d ") + form.cleaned_data['end_time'].strftime("%H:%M:%S")

            result = AgentCenter().agentDetail(env, user, col, start, end, mode)

            total_value = 0
            for d in result:
                total_value += d[5]

        return render(request, 'agentverifydetail.html', {
            'form': form,
            'result': result,
            'total_value': total_value,
            })
        # return JsonResponse(result_dict)
    else:
        form = AgentVerifyDetailForm()
        return render(request, 'agentverifydetail.html', {'form': form})




from .form import AutoWithdrawVerifyForm
from .FF_.AutoWithdrawVerify import AutoWithdrawVerify, checkFrontInput
@swagger_auto_schema(
    method='POST',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'env': openapi.Schema(type=openapi.TYPE_INTEGER),
            'orderID': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['env', 'orderID']
    ),
    responses={201: 'Searched', 400: 'Bad Request'}
)
@api_view(['POST', 'GET'])
def autoWithdrawVerify(request):
    if request.method == 'POST':
        form = AutoWithdrawVerifyForm(request.POST)
        if form.is_valid():
            env = int(form.cleaned_data['env'])
            orderID = str(form.cleaned_data['orderID'])
            if checkFrontInput().verifyOrder(orderID, env):
                withdraw = AutoWithdrawVerify(orderID, env=env)
                accountInfo = withdraw.getAccountInfo()
                redisPoints = withdraw.getRedisTimePoint()
                timePoints = withdraw.getCleanPointValue()

                verifyRrsult = withdraw.ruleCheck()

                ans = 0
                for i in range(len(verifyRrsult['switch'])):
                    if verifyRrsult['switch'][i] == 'On' and verifyRrsult[i+1]['result']:
                        ans = i+1
                        break

                stopRule = '全數通過'
                if set(verifyRrsult['switch']) == {'Off'}:
                    stopRule = '全部關閉，進入處理中'
                elif ans != 0:
                    stopRule = f'檢驗至Rule {ans} 時觸發'
                

                return render(request, 'auto_withdraw_verify.html',{
                    'form': form,
                    'stopRule': stopRule,
                    'verifyRrsult': verifyRrsult,
                    'accountInfo': accountInfo,
                    'redisPoints': redisPoints,
                    'timePoints': timePoints,
                    }
                )
            else:
                return render(request, 'auto_withdraw_verify.html', {'form': form, 'error_message': '訂單不存在'})
    else:
        form = AutoWithdrawVerifyForm()
        return render(request, 'auto_withdraw_verify.html', {'form': form})


@swagger_auto_schema(
    method='POST',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'env': openapi.Schema(type=openapi.TYPE_INTEGER),
            'user': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['env', 'user']
    ),
)
@api_view(['POST'])
def test_swagger(request):
    if request.method == 'POST':
        env = request.data['env']
        user= request.data['user']
        withdraw = AutoWithdrawVerify(user, env=env)
        res = withdraw.ruleCheck()
        
        return JsonResponse(res)

from .form import getGoogleAuthenticatorForm
from .FF_.googleAuthenticator import get_totp_token
from .FF_.Connection import MysqlConnection
@api_view(['POST', 'GET'])
def getGoogleAuthenticator(request):
    if request.method == 'POST':
        form = getGoogleAuthenticatorForm(request.POST)
        if form.is_valid():
            env = int(form.cleaned_data['env'])
            user = str(form.cleaned_data['user'])
            user_type = int(form.cleaned_data['user_type'])
            if env == 3:
                db_ = 'ubit_stg'
            elif env == 4:
                db_ = 'tgbet_stg'
                user_type = 1
            else:
                db_ = ''

            key = MysqlConnection(env).getGoogleAutKey(db_, user, user_type)

            if not key:
                auth_code = '這個人沒有綁定GOOGLE驗證喔'
            else:
                auth_code = get_totp_token(key)

            return render(request, 'getGoogleAuthenticator.html',
                                 {'form': form, 'auth_code': auth_code}
                                 )

    else:
        form = getGoogleAuthenticatorForm()
        return render(request, 'getGoogleAuthenticator.html', {'form': form})
      






    
        
    
    
        
        