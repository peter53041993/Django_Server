from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns # URL 添加可選的格式後綴


urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetListG.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetailG.as_view(), name='snippet-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    path('test/', views.test, name='test-api'),
    path('trunk_test/', views.trunk_config, name='trunk_test'),
    path('trunk_test/<str:unittype>/', views.trunk_test),
    path('creatUser/', views.createUser),
    path('test0910/', views.test_form),
    path('getAvlBal/', views.getAvlBal),
    path('activity531rank/', views.activity531),
    path('freeIp/', views.freeIpBlock),
]



# URL 添加可選的格式後綴
urlpatterns = format_suffix_patterns(urlpatterns)

