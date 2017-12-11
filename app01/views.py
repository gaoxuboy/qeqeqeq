from django.shortcuts import render, redirect, HttpResponse
# from app01 import models
# Create your views here.
import random
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Avg, Sum, Min, Max, Count

from django.contrib.auth import authenticate, login, logout

import json
from app01 import forms
from app01.models import UserInfo
from blog import settings
from app01.models import *
from django.db.models import F,Q


#+++++++++++++++++++++++++++++++++++++settings 配置路径 +++++++++
def func_class(request):
    return {'func':settings.FUNC_OBJ}
#+++++++++++++++++++++++++++++++++++++主页面 ++++++++++++++++++++
def index(request, **kwargs):
    obj = request.user
    type_list = Article.type_choices  #
    # print(kwargs)
    type_list_obj = int(kwargs.get('article_type_id', 0))
    # print(type_list_obj)
    # type_choice=models.Article.objects.filter(article_type_id=type_list_obj)
    # 方式2：

    # article_list = models.Article.objects.filter(**kwargs)#相当于定义的名字和models里面过滤的名字是一样的
    book_list = Article.objects.all()
    p_obj = Paginator(book_list, 4)
    obj_num = request.GET.get('page',1)
    try:
        list_all = p_obj.page(obj_num)
    except EmptyPage:
        list_all = p_obj.page(p_obj.num_pages)
    except PageNotAnInteger:
        list_all = p_obj.page(1)
    return render(request, 'index.html', {'type_list': type_list, 'type_list_obj': type_list_obj, 'obj': obj,'book_list':book_list ,'list_all':list_all,'list_all':list_all})
# ++++++++++++++++++++++++++++++++++++登录页面+++++++++++++++++++
def log_in(request):
    # meggage={'user':None,'error':''}
    if request.is_ajax():
        # if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        Verification = request.POST.get('Verification')
        print(username, password, Verification)
        meggage = {'user': None, 'error': ''}
        if Verification.upper() == request.session.get('valid_code').upper():

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                meggage['user'] = request.user.username
                print('=============', request.user.username)
            else:
                meggage['error'] = '用户名和密码错误'
        else:
            meggage['error'] = '验证码错误'

        return HttpResponse(json.dumps(meggage))

    return render(request, 'login.html')





    # return render(request,'login.html')
# ++++++++++++++++++++++++++++++++++++验证码页面++++++++++++++++++
def imger(request):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import random
    f = BytesIO()
    img = Image.new(mode='RGB', size=(120, 30),
                    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(img, mode='RGB')
    font = ImageFont.truetype("app01/static/bootstrap/fonts/kumo.ttf", 28)
    code_list = []
    for i in range(5):
        char = random.choice([chr(random.randint(65, 90)), str(random.randint(1, 9))])
        code_list.append(char)
        draw.text([i * 24, 0], char, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                  font=font)

    img.save(f, "png")

    valid_code = ''.join(code_list)

    request.session["valid_code"] = valid_code

    return HttpResponse(f.getvalue())
# +++++++++++++++++++++++++++++=++++++删除页面++++++++++++++++++++
def dell(request):
    logout(request)
    return redirect('/index/')
#+++++++++++++++++++++++++++++++++++++注册页面++++++++++++++++++++
def register(request):

    if request.method=='POST':
        form_obj = forms.Form(request,request.POST)  # 实例化对象，传入值
    #     message={'flag':False,'error':''}
    #     if form_obj.is_valid():
    #         print(123)
    #         message['flag']=True
    #     else:
    #         errors=form_obj.errors
    #         message['error']=errors
    #         print(errors)
    #     return HttpResponse(json.dumps(message))

        if form_obj.is_valid():
            print(form_obj.cleaned_data)
            username=form_obj.cleaned_data['username']#变量命名必须与数据库是一致的
            password = form_obj.cleaned_data['password']
            email = form_obj.cleaned_data['email']
            imger=request.FILES.get('img')
            print(1212121)

            UserInfo.objects.create_user(username=username,password=password,email=email,avatar=imger)

            return HttpResponse(True)
        else:
            errors = form_obj.errors
            # print(errors)
            # print(request.session["valid_code"])

        return HttpResponse(json.dumps(errors))

    form_obj = forms.Form(request)
    return render(request, 'register.html', {'form_obj': form_obj})
#+++++++++++++++++++++++++++++++++++++egon个人页面++++++++++++++++++++
def homgsite(request,user_site,**kwargs):
    #首先判断,指的是后缀的名字
    user=UserInfo.objects.filter(username=user_site).first()#匹配的是网站后缀，过滤是可以自定义，上面是以输入名字为自定义的.
    if not user:

        return render(request,'not.html')
    # print(user.fans)
    #拿到后缀名字，之后获取后缀名的个人博客信息
    blog_name=Blog.objects.filter(user=user).first()#egon个人博客
    # print('++++++++++++',blog_name)
    #获取博客信息之后，看博客里面有多少文章app01_comment
    article_name=Article.objects.filter(blog=blog_name)#获取的是engo写的文章信息
    # print('________',article_name)
    category_name=Category.objects.filter(blog=blog_name)# 获取的是egon所写的个人文章分类
    #print('>>>>>>>>>',category_name)<QuerySet [<Category: linux>, <Category: python>, <Category: go>, <Category: java>]>
    #每个分类下面文章的个数
    categoryRet=Article.objects.filter(blog=blog_name).values_list('category__title','category__nid').annotate(Count('nid'))
    # print(article_count)
    # <QuerySet [('go', 1), ('java', 1), ('linux', 1)]>
    #查询每个标签对象的文章个数
    tag_name=Tag.objects.filter(blog=blog_name)
    # print('+++++++++',tag_name)
    tagName=Article.objects.filter(blog=blog_name).values_list('tags__title','tags__nid').annotate(Count('nid'))
    # print('-----------------',tagName)#<QuerySet [('go自动化', 1), ('linux自动化', 1), ('python自动化', 1)]>
    # print(tagName)
    #日期分类
    article_time=Article.objects.filter(blog=blog_name).values('create_time')
    # print(article_time)
    article_time_list=[i['create_time'].strftime('%Y-%d-%m')for i in article_time]
    l = []
    for i in article_time_list:

        if ([i,article_time_list.count(i)]) not in l:
            l.append([i,article_time_list.count(i)])
    # print(l)

    #每个时间段有多少个文章
    create_time= [i['create_time'].strftime('%Y-%d-%m') for i in article_time]
    all=Article.objects.filter(blog=blog_name).values('create_time').annotate(Count('nid'))

    # print('////////',all)
    # print(kwargs)
    # print(kwargs)

    coment=kwargs.get('condition')
    if coment=='category':
        article_name= Article.objects.filter(blog=blog_name,category_id=kwargs.get('para'))
        # coment = kwargs.get('condition')
    elif coment == 'tag':
        article_name = Article.objects.filter(blog=blog_name,tags__nid=kwargs.get('para'))
    elif coment == 'data':
        article_name = Article.objects.filter(blog=blog_name, create_time=kwargs.get('para'))

        print(article_name)




    return render(request,'homgsite.html',locals())
#+++++++++++++++++++++++++++++++++++++egon文章内容显示++++++++++++++
def useregon(request,user_site,active_id):
    user = UserInfo.objects.filter(username=user_site).first()  # 匹配的是网站后缀，过滤是可以自定义，上面是以输入名字为自定义的.
    if not user:
        return render(request, 'not.html')
    active_obj=Article.objects.filter(nid=active_id).first()#主要是显示文章的信息，
    blog_name = Blog.objects.filter(user=user).first()  # egon个人博客
    # print('++++++++++++',blog_name)
    # 获取博客信息之后，看博客里面有多少文章app01_comment
    article_name = Article.objects.filter(blog=blog_name)  # 获取的是engo写的文章信息
    # print('________',article_name)
    category_name = Category.objects.filter(blog=blog_name)  # 获取的是egon所写的个人文章分类
    # print('>>>>>>>>>',category_name)<QuerySet [<Category: linux>, <Category: python>, <Category: go>, <Category: java>]>
    # 每个分类下面文章的个数
    article_count = Article.objects.filter(blog=blog_name).values_list('category__title','category__nid').annotate(Count('nid'))
    # print(article_count)<QuerySet [('go', 1), ('java', 1), ('linux', 1)]>
    # 查询每个标签对象的文章个数
    tag_name = Tag.objects.filter(blog=blog_name)
    # print('+++++++++',tag_name)
    tagName = Article.objects.filter(blog=blog_name).values_list('tags__title').annotate(Count('nid'))
    # print('-----------------',tagName)#<QuerySet [('go自动化', 1), ('linux自动化', 1), ('python自动化', 1)]>
    # 日期分类
    article_time = Article.objects.filter(blog=blog_name).values('create_time')
    # print(article_time)
    article_time_list = [i['create_time'].strftime('%Y-%d-%m') for i in article_time]
    l = []
    for i in article_time_list:

        if ([i, article_time_list.count(i)]) not in l:
            l.append([i, article_time_list.count(i)])
            # print(l)

    comment_obj=Comment.objects.filter(article_id=active_obj)
    return render(request, 'useregon.html',locals())

#++++++++++++++++++++++++++++++++++++++点赞功能实现++++++++++++++++++++
def poll(requerst):
    user_id=requerst.user.nid  #取出的是点赞人的id
    active_id=requerst.POST.get('active_id') #取出的是文章的id
    response={'flag':True}
    if  ArticleUpDown.objects.filter(user_id=user_id,article_id=active_id):
        response['flag'] = False
    else:
        ArticleUpDown.objects.create(user_id=user_id,article_id=active_id)
        Article.objects.filter(nid=active_id).update(up_count=F('up_count')+1)

    return HttpResponse(json.dumps(response))

#++++++++++++++++++++++++++++++++++++++不支持功能实现+++++++++++++====
def updown(request):

    user_nid=request.user.nid
    active_id=request.POST.get('active_id')
    response={'flag':True}
    if CommentUp.objects.filter(article_id=active_id,user_id=user_nid):
        response['flag']=False
    else:
        CommentUp.objects.create(article_id=active_id,user_id=user_nid)
        Article.objects.filter(nid=active_id).update(down_count=F('down_count')+1)

    return HttpResponse(json.dumps(response))

#++++++++++++++++++++++++++++++++++++++评论功能++++++++++++++++++++++++
def comment(request):
    user_id=request.user
    article_id=request.POST.get('article_id')
    countent=request.POST.get('countent')
    father_id=request.POST.get('father_id')
    # print(request.user)
    # print(type(request.user))
    errors={}
    if not user_id.username:
        errors['error']=True
        return HttpResponse(json.dumps(errors))
    else:
        if father_id:
            comment_obj=Comment.objects.create(user_id=user_id.nid,article_id=article_id,content=countent,parent_id_id=father_id)
        else:
            comment_obj = Comment.objects.create(user_id=user_id.nid, article_id=article_id, content=countent,)


    Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)
    response={'comment_time':str(comment_obj.create_time)[:16]}
    # print(response)

    return HttpResponse(json.dumps(response))
# +++++++++++++++++++++++++++++++++++++增加随笔++++++++++++++++++++++
def addarticle(request):
    # print(request)
    category=Category.objects.all()
    tag=Tag.objects.all()
    article_obj=Article.type_choices
    # print(request.user)
    user=UserInfo.objects.filter(username=request.user).first()
    blog_obj=user.blog.nid


    # print(user)
    if request.method=='POST':
        title=request.POST.get('title')
        articls=request.POST.get('article_content')
        category=request.POST.get('category')
        tag=request.POST.get('tag')
        print(tag)
        type_obj=request.POST.get('obj')
        # print(type_obj)
        article= Article.objects.create(title=title,category_id=category,article_type_id=type_obj,blog_id=blog_obj)
        # Article.objects.filter()
        ArticleDetail.objects.create(content=articls,article=article)
        # 标签添加没有写，记得写完
        # tag2=Tag.objects.filter(nid=tag)
        # article.Article2Tag.add(*[tag2,article])
        # print(tag2)
        # print(type(tag2))

        return redirect('/management/')

    return render(request,'addarticle.html',locals())

#+++++++++++++++++++++++++++++++++++++++上传文件++++++++++++++++++++++++++
def filename(request):


    print(request.FILES)
    file_obj=request.FILES.get('imgFile')
    # < MultiValueDict: {'imgFile': [ < InMemoryUploadedFile: u = 3128597575, 2744814604 & fm = 27 & gp = 0.j
    # pg(image / jpeg) >]} >
    filename=file_obj.name#name属于文件里面的属性 还有大小size‘
    with open('app01/media/upload/img/'+filename,'wb') as f:#拼接的路径
        for chunk in file_obj.chunks():#后面2步for循环 主要是循环取出上传文件的内容
            f.write(chunk)

      #接收完之后，我们同时要让客户能在前端进行预览，所以要给前端发数据
    response_put={
        'error':0,
        'url':'/media/upload/img/'+filename

    }

    return HttpResponse(json.dumps(response_put))
#++++++++++++++++++++++++++++++++++++++后台管理+++++++++++++++++++++++++++
def management(request):
    user = UserInfo.objects.filter(username=request.user)
    blog_obj = Blog.objects.filter(user=user)
    article_obj = Article.objects.filter(blog=blog_obj)
    # article_obj =Article.objects.all()
    p_obj = Paginator(article_obj,6)
    obj_num = request.GET.get('page',1)
    try:
        article_obj = p_obj.page(obj_num)
    except EmptyPage:
        article_obj = p_obj.page(p_obj.num_pages)
    except PageNotAnInteger:
        article_obj = p_obj.page(1)

    # article_obj=Article.objects.filter(username=request.user)
    print(request.user)



    return render(request,'management.html',locals())

#++++++++++++++++++++++++++++++++++++==删除文章++++++++++++++++++++++++++++
def del2(request):
    if request.is_ajax():
        title=request.POST.get('title')

    title=Article.objects.filter(title=title).delete()

    return HttpResponse('ok')
#++++++++++++++++++++++++++++++++++++++评论点赞++++++++++++++++++++++++++++
def commentup(request):
    # print(1111111)
    active_id=request.POST.get('active_id')
    user_id=request.POST.get('user_id')
    # print(user_id)
    comment_id=request.POST.get('comment_id')

    response={'flag':False}
    if CommentUp.objects.filter(article_id=active_id,comment_id=comment_id):
        response['flag']=True

    else:

        CommentUp.objects.create(article_id=active_id,comment_id=comment_id)
        Comment.objects.filter(nid=comment_id).update(up_count=F('up_count')+1)
        # print(32424232)

    # printup_count

    return HttpResponse(json.dumps(response))

#++++++++++++++++++++++++++++++++++++++修改密码++++++++++++++++++++++++++++
def mima(request):
    user = request.user

    # if request.is_ajax():
    old_password=request.POST.get('old_password')
    new_password=request.POST.get('new_password')
    inputPassword=request.POST.get('inputPassword')
    # print(2324)
    state='OK'
    if user.check_password(old_password):
        print(4333333333333)
        state=''
        if  new_password==''or old_password=='':
            state='请输入新的密码'
        elif new_password != inputPassword:
            state='密码输入不一致'
        else:
            user.set_password(new_password)
            user.save()
            state='修改密码成功'
        return HttpResponse('state')


    print(1313131)

    return render(request,'mima.html',{'state':state})

