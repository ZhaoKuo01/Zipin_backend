from django.core import mail
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from celery_task import send_email
from . import functions
from . import functions
from .check_result import check_result
from .serializers import NoteSerializer, UserinfoSerializer, MaincomnSerializer, SubcomnSerializer, \
    MycollectionSerializer, MylikeSerializer
from .models import Note, Userinfo, Maincomn, Subcomn, MyCollection, MyLike, NoteImage
from django.http import response, JsonResponse
from .form import Imageform
import random
from drf_multiple_model.views import ObjectMultipleModelAPIView


# Create your views here.
# 获取路由表
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Hoem page'
        },
        {
            'Endpoint': '/notes/id/update',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Update'
        },
        {
            'Endpoint': '/notes/id/create',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Create'
        },
    ]
    return Response(routes)


# 获取所有的数据
@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUsers(request):
    users = Userinfo.objects.all()
    serializer = UserinfoSerializer(users, many=True)
    return Response(serializer.data)


@csrf_exempt
def checkmail(request):
    email = request.POST.get['email']
    checkcode = ''
    for i in range(4):
        a = random.randint(0, 9)
        b = str(a)
        checkcode = checkcode + b
    mail.send_mail(
        subject="测试邮件",
        message=f"你好，你的登陆验证码是{checkcode}",
        from_email="825840132@qq.com",
        recipient_list=[email],
    )


@csrf_exempt
@api_view(['POST'])
def createUser(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        data = request.POST
        username = data['user']
        email = data['email']
        password = data['pwd']
        password2 = data['pwd2']
        # 手机号后面再认证
        phone = 123456
        # print(len(data['user']))
        if Userinfo.objects.filter(email=email):
            errormsg = "邮箱已存在"
            return JsonResponse({
                "errormsg": errormsg,
            })
        if Userinfo.objects.filter(username=username):
            errormsg = "用户名已存在"
            return JsonResponse({
                "errormsg": errormsg,
            })
        if password != password2:
            errormsg = "两次输入密码不一致"
            return JsonResponse({
                "errmsg":errormsg,
            })
        if 3 <= len(data['user']) <= 12:
            if username.isalnum():
                if 8 <= len(password) <= 20 and not password.isdigit() and not password.islower():
                    user = Userinfo.objects.create(
                        username=username,
                        email=email,
                        password=password,
                        phone=phone,
                    )

                    request.session['username'] = username
                    request.session['password'] = password
                    request.session['is_login'] = True

                    serialiezer = UserinfoSerializer(user, many=False)

                    msg = "注册成功，请登陆邮箱验证"
                    result = send_email.delay(user.id)
                    print(check_result(result))
                    return JsonResponse({
                        "result": msg,
                        "data": serialiezer.data,
                    })
                else:
                    errormsg = "密码应当8-20位且包含大小写字母、数字"
                    return JsonResponse({
                        "errormsg": errormsg,
                    })

                    # return render(request, "signup.html", {"errormsg": errormsg})
            else:
                errormsg = "用户名中含有非法字符"
                print(errormsg)
                return JsonResponse({
                    "errormsg": errormsg,
                })
                # return render(request, "signup.html", {"errormsg": errormsg})
        else:
            errormsg = "请输入3至12位用户名"
            print(errormsg)

        # if phone.isdigit():
        #     if len(password) != 11 or password[:2] not in ["13", "15", "18", "19"]:
        #         errormsg = "请输入正确手机号"
        #         return render("request", "signup.html", {"errormsg": errormsg})


def active_user(request):
    uid = request.GET.get('id')
    user = Userinfo.objects.filter(id=uid).update(is_active=1)
    serializer = UserinfoSerializer(user, many=False)
    return JsonResponse(serializer)


# 获取特定的数据
@api_view(['GET'])
def getNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getMaincomn(request, pk):
    comn = Maincomn.objects.filter(pa_id=pk)
    serializer = MaincomnSerializer(comn, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSubcomn(request, pk):
    comn = Subcomn.objects.filter(m_id=pk)
    serializer = SubcomnSerializer(comn, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getcollec(request, pk):
    coll = MyCollection.objects.filter(user=pk)
    serializer = MycollectionSerializer(coll, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getlike(request, pk):
    like = MyLike.objects.filter(user=pk)
    serializer = MylikeSerializer(like, many=True)
    return Response(serializer.data)


def getDetail(request, pk):
    if request.method == "GET":
        note = Note.objects.get(id=pk)
        user = Userinfo.objects.get(id=note.au_id)
        maincomns = Maincomn.objects.filter(pa_id=pk)
        subcomn = Subcomn.objects.filter(pa_id=pk)
        # try:
        #     maincomns = Maincomn.objects.filter(pa_id=pk)
        #
        #     try:
        #         subcomn = Subcomn.objects.filter(pa_id=pk)
        #     except Subcomn.DoesNotExist:
        #         return render(request, "notepage.html", {"note": note, "user": user, "maincomn": maincomns})
        # except Maincomn.DoesNotExist:
        #     return render(request, "notepage.html", {"note": note, "user": user})
        # return render(request, "notepage.html",
        #               {"note": note, "user": user, "maincomn": maincomns, "subcomn": subcomn})
        serializer1 = NoteSerializer(note, many=False)
        serializer2 = UserinfoSerializer(user, many=False)
        serializer3 = MaincomnSerializer(maincomns, many=True)
        serializer4 = SubcomnSerializer(subcomn, many=True)

        return JsonResponse({
            "user": serializer2.data,
            "note": serializer1.data,
            "maincomn": serializer3.data,
            "subcomn": serializer4.data,
        })


# 创建
@api_view(['POST'])
@csrf_exempt
def create(request):
    if request.method == "GET":
        return render(request, "newnote.html")
    if request.method == "POST":
        user = Userinfo.objects.get(username=request.session.get('username'))
        # image = request.FILES.get('image')
        data = request.POST
        body = data['body']
        title = data['title']
        tag = data['tag']
        errmsg = ''
        if len(title)<2 or len(title)>15 or not title.isalnum():
            errmsg="标题不符合要求"
            return JsonResponse({
                "errmsg":errmsg
            })
        if len(body)<=1:
            errmsg="文章内容不能为空"
            return JsonResponse({
                "errmsg":errmsg
            })
        elif len(body)>300:
            errmsg="文章内容过长"
            return JsonResponse({
                "errmsg":errmsg
            })
        note = Note.objects.create(
            au_id=user.id,
            body=body,
            title=title,
            tag=tag,
            like_num=0,
            coll_num=0,
        )
        # NoteImage.objects.create(
        #     note=note,
        #     image=image,
        # )
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
        # return redirect("/homepage")


# 创建主评论
@api_view(['POST'])
@csrf_exempt
def createMaincomn(request, pk):
    user = Userinfo.objects.get(username=request.session.get("username"))
    pa_id = pk
    username = user.username
    uid = user.id
    data = request.data
    # content = request.POST.get("content")
    content = data['content']
    if len(content)<1 or len(content)>90:
        return JsonResponse({
            "errmsg":"内容长度不符合要求"
        })
    maincomn = Maincomn.objects.create(
        pa_id=pa_id,
        # 评论发布者用户名
        u_name=username,
        # 评论发布者id
        u_id=uid,

        content=content,
        like_num=0,
    )
    serializer = MaincomnSerializer(maincomn, many=False)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def createSubcomn(request, pk):
    user = Userinfo.objects.get(username=request.session.get("username"))
    mainconmn = Maincomn.objects.get(id=pk)
    data = request.data
    # content = request.POST.get("content")
    content = data['content']
    if len(content)<1 or len(content)>90:
        return JsonResponse({
            "errmsg":"内容长度不符合要求"
        })
    subcomn = Subcomn.objects.create(
        pa_id=mainconmn.pa_id,
        m_id=mainconmn.id,
        u_name=user.username,
        u_id=user.id,
        content=content,
        like_num=0
    )

    # pa_id = Maincomn.objects.get(id=pk).pa_id
    # return redirect("/notedetail/%d/" % pa_id)
    serializer = SubcomnSerializer(subcomn, many=False)
    return Response(serializer.data)


# 更新
@api_view(['PUT'])
def update(request, pk):
    data = request.data
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# 装饰器检查用户是否登陆
def check_login(func):
    def inner(request, *args, **kwargs):
        next_url = request.get_full_path()
        # 获取session用于判断是否登陆
        if request.session.get('is_login'):
            return func(request, *args, **kwargs)
        else:
            # 跳转到登陆页面
            return redirect()

    return inner


@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        data = request.POST
        username = data['user']
        passwd = data['pwd']
        # username = request.POST.get("user")
        # passwd = request.POST.get("pwd")
        user = Userinfo.objects.get(username=username)
        if username == user.username and passwd == user.password:
            print("正确")
            request.session['user_id'] = user.id
            request.session['username'] = username
            request.session['password'] = passwd
            request.session['is_login'] = True
            print(request.session.keys())

        else:
            error_msg = '登陆验证失败'
            # return render(request, "login.html",
            #               {'login_error_msg': error_msg,
            #                'next_url': next_url,
            #                'user': username,
            #                'pwd': passwd})
            return JsonResponse({"err_msg": error_msg})
        # return render(request, "index.html", {'username': request.session.get('username')})
        # return redirect('../homepage')
        serializer = UserinfoSerializer(user, many=False)
        return JsonResponse(serializer.data)


def homepage(request):
    if request.method == "GET":
        notes = Note.objects.all()
        return render(request, "index.html", {"notes": notes})


def logout(request):
    rep = redirect("/homepage/")
    if 'is_login' in request.session:
        request.session.clear()
    return rep


@check_login
def index(request):
    return render(request, "index.html")


# 删除
@api_view(['DELETE'])
def delete(request, pk):
    image = NoteImage.objects.filter(note=pk)
    image.delete()
    note = Note.objects.get(id=pk)
    note.delete()
    maincomn = Maincomn.objects.filter(pa_id=pk)
    maincomn.delete()
    subcomn = Maincomn.objects.filter(pa_id=pk)
    subcomn.delete()
    return JsonResponse({
        "msg": "success"
    })


# 收藏功能
def collect(request, pk):
    note = Note.objects.get(id=pk)
    username = request.session.get("username")
    user = Userinfo.objects.get(username=username)
    collect_list = MyCollection.objects.filter(user=user.id)
    if collect_list.filter(note=note.id):
        collect_list.filter(note=note.id).delete()
        note.coll_num = note.coll_num - 1
        note.save()
        return JsonResponse({
            "collect": "cancel"
        })
    else:
        MyCollection.objects.create(
            user=user,
            note=note,
        )
        note.coll_num = note.coll_num + 1
        note.save()
        return JsonResponse({"collect": "success"})


def identify(request):
    user = Userinfo.objects.filter(username=request.session.get("username")).first()
    if user.is_active == 1:
        user.identity = "wait"
        user.save()
        msg = "认证成功"
        return JsonResponse({
            "msg": msg
        })
    msg = "不具备资格"
    return JsonResponse({
        "msg": msg
    })


def giveidentity(request, pk):
    user = Userinfo.objects.filter(id=pk).first()
    user.identity = "poster"
    user.save()
    msg = "设置成功"
    return JsonResponse({
        "msg": msg
    })
