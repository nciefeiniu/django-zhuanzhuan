"""
@UpdateTime: 2017/12/7
@Author: liutao
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django import forms
from .models import User,Product,Images
from django.http import HttpResponseRedirect
import random
import os

#上传图片存储位置
path = 'static/up_images/'

# Create your views here.
def index(request):
    #生成首页随机的产品展示
    count = Product.objects.count()

    if count<5:
        phones = Product.objects.raw(
            'select p.*,i.*,u.u_id,u.u_name,u.u_touxiang from product p left join images i on p.p_id=i.p_id left join user u on u.u_id=p.u_id limit 5 ')
        return render(request, 'xianyu/index.html', {'phones': phones})
    else:
        num = random.randint(0,count-5)
        phones = Product.objects.raw(
                'select p.*,i.*,u.u_id,u.u_name,u.u_touxiang from product p left join images i on p.p_id=i.p_id left join user u on u.u_id=p.u_id limit '+str(num)+','+str(num+5))
        return render(request, 'xianyu/index.html', {'phones':phones})

#登录/注册表单
class Form(forms.Form):
    username = forms.CharField(label="帐号 ", max_length=100)
    password = forms.CharField(label="密码 ", widget=forms.PasswordInput())

#搜索表单
class Form_search(forms.Form):
    p_name = forms.CharField( max_length=40, label='', widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder':"请输入类别或关键字"}))

#发布商品表单
#class Form_addproduct(forms.Form):
#    p_name = forms.CharField()
#    p_money = forms.

#注册
def signup(request):
    Method = request.method
    if Method == 'POST':
        sf = Form(request.POST)
        if sf.is_valid():
            username = sf.cleaned_data['username']
            password = sf.cleaned_data['password']
            userhas = User.objects.filter(u_name=username)
            print(len(userhas))
            print(username)
            if len(userhas) != 0:
                return render(request, 'xianyu/signup.html', {'sf':sf, 'tip':'用户名存在' })
            else:
                registAdd = User.objects.get_or_create(u_name=username, u_passwd=password)
                if registAdd == False:
                    return HttpResponse("出错 ")
                else:
                    return HttpResponseRedirect("/xianyu/login")
    else:
        sf = Form()
        return  render(request, 'xianyu/signup.html', {'sf':sf})

#登陆
def login(request):
    if request.method == 'POST':
        sf = Form(request.POST)
        if sf.is_valid():
            # 获取表单用户密码
            username = sf.cleaned_data['username']
            password = sf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(u_name=username, u_passwd=password)
            if user:
                # 比较成功，跳转index
                request.session.set_expiry(3600)
                request.session['username'] = username
                return HttpResponseRedirect('/xianyu/')
            else:
                # 比较失败，还在login
                sf = Form()
                return render(request, 'xianyu/login.html', {'sf': sf, 'tip':'账号或密码错误！'})
    else:
        sf = Form()
        return render(request, 'xianyu/login.html', {'sf':sf})

#注销
def exit(request):
    del request.session['username']
    return HttpResponseRedirect("/xianyu/")

#手机类别界面
def moblephone(request):
    if 'username' in request.session:
        uname = "欢迎 "+request.session['username']
        si = "注销";
        n_url = ""
        s_url = "/xianyu/exit/"
    else:
        uname = "登录"
        si = "注册";
        n_url = "/xianyu/login/"
        s_url = "/xianyu/signup/"
    #查询数据库中所有商品信息
    products = Product.objects.raw('select a.p_id,a.p_name,a.p_money,a.p_number,a.p_info,b.img_address,c.u_name,c.u_touxiang from product a, images b, user c where a.p_id=b.p_id and a.u_id=c.u_id; ')
    #返回搜索框和数据
    fs = Form_search()
    return  render(request, 'xianyu/phone.html',{'fs': fs, 'products': products, 'username':uname, 'signup':si, 'n_url':n_url, 's_url':s_url})

#商品详情界面
def detail(request):
    if 'username' in request.session:
        uname = "欢迎 "+request.session['username']
        si = "注销";
        n_url = ""
        s_url = "/xianyu/exit/"
    else:
        uname = "登录"
        si = "注册";
        n_url = "/xianyu/login/"
        s_url = "/xianyu/signup/"
    fs = Form_search()
    p_id = request.GET['pid']
    has_product = Product.objects.filter(p_id=p_id)
    if has_product:
        product = Product.objects.raw(
            'select p.*,i.*,u.u_id,u.u_name,u.u_touxiang from product p left join images i on p.p_id=i.p_id left join user u on u.u_id=p.u_id where p.p_id = '+p_id+'; ')
        print(product)
        return render(request, 'xianyu/detail.html', {'fs':fs, 'product': product, 'username':uname, 'signup':si, 'n_url':n_url, 's_url':s_url})

    else:
        template = get_template('xianyu/404.html')
        html = template.render(locals())
        return HttpResponse(html)

#添加商品
def addproduct(request):
    if 'username' in request.session:
        uname = "欢迎 " + request.session['username']
        si = "注销";
        n_url = ""
        s_url = "/xianyu/exit/"

        if request.method == 'POST':
            u_id = User.objects.get(u_name=request.session['username']).u_id
            p_name = request.POST['biaoti']
            p_money = request.POST['jiage']
            p_num = request.POST['shuliang']
            p_info = request.POST['jieshao']
            obj = request.FILES.get('up_img')
            #上传图片到static/up_images
            img_name = str(random.randint(10000,99999))+obj.name
            f = open(os.path.join(path, str(img_name)), 'wb')
            for line in obj.chunks():
                f.write(line)
            f.close()
            #写入数据库
            w_db_p = Product(p_name=p_name, p_money=p_money, p_number=p_num,p_info=p_info,u_id=u_id)
            w_db_p.save()
            print(w_db_p.p_id)
            w_db_img = Images(img_address="/static/up_images/"+img_name, p_id=w_db_p.p_id)
            w_db_img.save()
        else:
            return render(request, 'xianyu/salepost.html',
                          { 'username': uname, 'signup': si, 'n_url': n_url,
                           's_url': s_url})
    else:
        return HttpResponseRedirect("/xianyu/login")

