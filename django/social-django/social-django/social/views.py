from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from .models import Member, Profile, Message  # python3新增加的功能
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

appname = 'Facemagazine'


def index(request):  # 建立链接索引
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
        'appname': appname,
        })
    return HttpResponse(template.render(context))


def messages(request):  # 返回登陆状态
    if 'username' in request.session:
        username = request.session['username']
        template = loader.get_template('social/messages.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': username,
                'loggedin': True
                })

        return HttpResponse(template.render(context))
    else:
        raise Http404("User is not logged it, no access to messages page!")


def signup(request):  # 注册链接
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
        'appname': appname,
        })
    return HttpResponse(template.render(context))


def register(request):  # 注册
    u = request.POST['user']
    p = request.POST['pass']
    user = Member(username=u, password=p)
    user.save()
    template = loader.get_template('social/user-registered.html')    
    context = RequestContext(request, {
        'appname': appname,
        'username': u
        })
    return HttpResponse(template.render(context))


def login(request):  # 登陆
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            raise Http404("User does not exist")
        if member.password == p:
            request.session['username'] = u
            request.session['password'] = p
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            raise Http404("Incorrect password")


def logout(request):  # 退出账户
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        raise Http404("Can't logout, you are not logged in")


def member(request, view_user):  # 会员附加信息
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'social/member.html', {
            'appname': appname,
            'username': username,
            'greeting': greeting,
            'profile': text,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to members page!")


def friends(request):  # 朋友状况
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'social/friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to members page!")


def members(request):  # 会员朋友关系
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # follow new friend
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        # unfollow a friend
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        # view user profile
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            # list of all other members
            members = Member.objects.exclude(pk=username)
            # list of people I'm following
            following = member_obj.following.all()
            # list of people that are following me
            followers = Member.objects.filter(following__username=username)
            # render reponse
            return render(request, 'social/members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                )
    else:
        raise Http404("User is not logged it, no access to members page!")


def profile(request):  # 会员附加信息
    if 'username' in request.session:
        u = request.session['username']
        member = Member.objects.get(pk=u)
        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'social/profile.html', {
            'appname': appname,
            'username': u,
            'text': text,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to profiles!")


def checkuser(request):  # 查看是否登陆
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        else:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")

# 加载信息view


def message(request):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=username)
        if request.method == 'POST':  # 如果是提交信息
            age = request.POST['age']
            sex = request.POST['sex']
            like = request.POST['like']
            if member.messages:  # 如果messages表存在，就直接赋值
                member.messages.age = age
                member.messages.sex = sex
                member.messages.like = like
            else:  # 如果表不存在就创建表
                messages = Message(age=age, sex=sex, like=like)
                messages.save()
                member.messages = messages
            member.save()

        else:  # 如果是查看信息
            if member.messages:  # 如果表存在就显示数据
                age = member.messages.age
                sex = member.messages.sex
                like = member.messages.like
            else:  # 表不存在就空着
                age = ""
                sex = ""
                like = ""
        return render(request, 'social/messages.html', {
            'appname': appname,
            'username': username,
            'age': age,
            'like': like,
            'sex': sex,
            'loggedin': True
        })
    else:
        raise Http404("You are not the user, no access to access to messages!")
##############################################add REST API############################################################'
'''from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer


class JSONResponse(HttpResponse):
        """
        将内容转为JSON格式的HttpResponse
        """
        def __init__(self, data, **kwargs):
            content = JSONRenderer().render(data)
            kwargs['content_type'] = 'application/json'
            super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
        """
        展示所有存在的snippet, 或建立新的snippet
        """
        if request.method == 'GET':
            snippets = Message.objects.all()
            serializer = MessageSerializer(snippets, many=True)
            return JSONResponse(serializer.data)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
@csrf_exempt
def snippet_detail(request, pk):
        """
        展示, 更新或删除一个snippet
        """
        username = request.session['username']
        try:
            snippet = Message.objects.get(pk=username)
        except Message.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = MessageSerializer(snippet)
            return JSONResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = MessageSerializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            snippet.delete()
            return HttpResponse(status=204)
'''
from rest_framework import authentication, permissions, viewsets

from .models import Message
from .serializers import MessageSerializer


class DefaultMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class MessageViewSet(viewsets.ModelViewSet):
        queryset = Message.objects.order_by('age')
        serializer_class = MessageSerializer
