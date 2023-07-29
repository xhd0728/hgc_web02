from django.shortcuts import render, redirect
from app01.utils import DB

# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('code')

    if code != '6982':
        return redirect('/login/')

    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
    _password = mysql.findone(
        f'select password from tab_user where username = "{username}"')['password']
    if password == _password:
        return render(request, 'index.html')
    return redirect('/login/')


def info(request):
    return render(request, 'info.html')


def pass_(request):
    return render(request, 'pass.html')


def page(request):
    return render(request, 'page.html')


def adv(request):
    return render(request, 'adv.html')


def book(request):
    return render(request, 'book.html')


def column(request):
    return render(request, 'column.html')


def list_(request):
    mysql = DB(host='127.0.0.1',
               user='root',
               passwd='10011010',
               db='hgx_web')
    sql = 'select * from tab_lol limit 20'
    res_list = mysql.findall(sql)
    return render(request, 'list.html', {'res_list': res_list})


def handle_delete(request):
    id = request.GET.get('id')
    mysql = DB(host='127.0.0.1',
               user='root',
               passwd='10011010',
               db='hgx_web')
    mysql.delete(
        f'delete from tab_lol where id = "{id}"')
    return redirect('/list/')


def show_update(request):
    id = request.GET.get('id')
    mysql = DB(host='127.0.0.1',
               user='root',
               passwd='10011010',
               db='hgx_web')
    result = mysql.findone(f'select * from tab_lol where id = "{id}"')
    return render(request, 'show_update.html', {'result': result})


def add(request):
    return render(request, 'add.html')


def cate(request):
    return render(request, 'cate.html')
