from django.shortcuts import render
from .forms import  RegistrationForm, LeginForm
from .models import Customer, Goods, OrderLineItem, Orders
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DeleteView
import random
import datetime
# Create your views here.

#註冊
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_customer = Customer()
            new_customer.id = form.cleaned_data['userid']
            new_customer.name = form.cleaned_data['name']
            new_customer.password = form.cleaned_data['password']
            new_customer.birthday = form.cleaned_data['birthday']
            new_customer.phone = form.cleaned_data['phone']

            new_customer.save()

            return render(request, 'customer_reg_success.html')
    else:
        form = RegistrationForm()
    return render(request, 'customer_reg.html', {'form': form})

#登入
def login(request):
    if request.method == 'POST':
        form = LeginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            c = Customer.objects.get(id=userid)

            if c is not None and c.password == password:
                #客戶ID放到http Session中
                request.session['customer_id'] = c.id
                return HttpResponseRedirect('main/')
    else:
        form = LeginForm()
    return render(request, 'login.html', {'form': form})

#主畫面
def main(request):
    #判斷用戶是否登入
    if not request.session.has_key('customer_id'):
        print('請登入')
        return HttpResponseRedirect('/login/')
    
    return render(request, 'main.html')



#商品列表
class GoodsListView(ListView):
    model = Goods
    ordering = ['id']
    template_name = 'goods_list.html'

#商品詳細
def show_goods_detail(request):
    goodsid = request.GET['id']
    goods = Goods.objects.get(id=goodsid)

    return render(request, 'goods_detail.html', {'goods': goods})

#添加購物車
def add_cart(request):
    if  not request.session.has_key('customer_id'):
        print('請先登入')
        return HttpResponseRedirect('/login/')
    
    goodsid = int(request.GET['id'])
    goodsname = request.GET['name']
    goodsprice = float(request.GET['price'])

    #判斷session是否已經存在購物車數據

    if not request.session.has_key('cart'):
        #如果沒有則創一個空的購物車,購物車是列表結構
        request.session['cart'] = []
    
    cart = request.session['cart']
    flag = 0
    for item in cart:
        #購物車結構 [商品id, 商品名稱, 商品價格, 數量]
        if item[0] == goodsid : #購物車如果有相同商品
            item[3] += 1
            flag = 1
            break

    if flag == 0: #當前購物車沒有相同商品
        item = [goodsid, goodsname, goodsprice,  1]
        cart.append(item)

    request.session['cart'] = cart
    
    print(cart)

    page = request.GET['page']
    if page == "detail":
        return HttpResponseRedirect('/detail/?id=' + str(goodsid) )
    else:
        return HttpResponseRedirect('/list/')

#查看購物車
def show_cart(request):
    #判斷是否登入
    if not request.session.has_key('customer_id'):
        print('請登入')
        return HttpResponseRedirect('/login/')
    if not request.session.has_key('cart'):
        return render(request, 'cart.html', {'list': [], 'total': 0})
    cart = request.session['cart']
    list = []
    total = 0.0
    for item in cart:
        #item結構 [商品ID, 商品名稱, 價格, 數量]
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)
    
    return render(request, 'cart.html', {'list': list, 'total': total})

#提交訂單
def submit_orders(request):
    if request.method == 'POST':
        #從表單中取出數據 添加到orders模型對象
        orders = Orders()
        #生成訂單id,當前時間+隨機數字
        n = random.randint(0,9)
        d = datetime.datetime.today()
        ordersid = str(int(d.timestamp() * 1e6)) + str(n)
        orders.id = ordersid
        orders.order_date = d
        orders.status = 1
        orders.total = 0.0

        orders.save()

        cart = request.session['cart']
        total = 0.0

        for item in cart :
            #item結構 [商品ID, 商品名稱, 價格, 數量]
            goodsid = item[0]
            goods = Goods.objects.get(id=goodsid)
            
            quantity = request.POST['quantity_' + str(goodsid)]

            try:
                quantity = int(quantity)
            except:
                quantity = 0

            #計算小記
            subtotal = item[2] * quantity
            total += subtotal

            order_line_item = OrderLineItem()
            order_line_item.quantity = quantity
            order_line_item.goods = goods
            order_line_item.orders = orders
            order_line_item.sub_total = subtotal

            order_line_item.save()
        
        orders.total = total
        orders.save()

        #提交清除購物車

        del request.session['cart']

        return render(request, 'order_finish.html', {'ordersid': ordersid})
