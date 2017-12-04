from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django import forms
from .models import User,Product,Images
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    template = get_template('xianyu/index.html')
    html = template.render(locals())
    return HttpResponse(html)

#表单
class Form(forms.Form):
    username = forms.CharField(label="帐号 ", max_length=100)
    password = forms.CharField(label="密码 ", widget=forms.PasswordInput())

#搜索表单
class Form_search(forms.Form):
    p_name = forms.CharField( max_length=40, label='', widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder':"请输入类别或关键字"}))

#注册
def signup(request):
    Method = request.method
    if Method == 'POST':
        sf = Form(request.POST)
        if sf.is_valid():
            username = sf.cleaned_data['username']
            password = sf.cleaned_data['password']
            userhas = User.objects.get(u_name=username)
            if userhas != 0:
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

#手机类别界面
def moblephone(request):
    #查询数据库中所有商品信息
    products = Product.objects.raw('select a.p_id,a.p_name,a.p_money,a.p_number,a.p_info,b.img_address,c.u_name,c.u_touxiang from product a, images b, user c where a.p_id=b.p_id and a.u_id=c.u_id; ')

    #返回搜索框和数据
    fs = Form_search()
    return  render(request, 'xianyu/phone.html',{'fs': fs, 'products': products})

#商品详情界面
def detail(request):
    fs = Form_search()
    p_id = request.GET['pid']
    has_product = Product.objects.filter(p_id=p_id)
    if has_product:
        product = Product.objects.raw(
            'select a.p_id,a.p_name,a.p_money,a.p_number,a.p_info,b.img_address,c.u_name,c.u_touxiang from product a, images b, user c where a.p_id='+p_id+' and b.p_id='+p_id+'; ')
        print(product)
        return render(request, 'xianyu/detail.html', {'fs':fs, 'product': product})

    else:
        template = get_template('xianyu/404.html')
        html = template.render(locals())
        return HttpResponse(html)
