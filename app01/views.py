from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from app01.utils import DB, set_hash, handle_page
import os


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
        return redirect('/index/')
    return redirect('/login/')


def index(request):
    return render(request, 'index.html')


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
    page = int(request.GET.get('page', 1))
    total_count = len(mysql.findall('select id from tab_lol'))
    page_size = 10
    start = (page-1)*page_size
    res_list = mysql.findall(
        f'select * from tab_lol limit {start},{page_size}')
    page_string = handle_page(page, total_count, page_size)
    return render(request, 'list.html', {'res_list': res_list, 'page_string': page_string})


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


def handle_update(request):
    id = request.POST.get('id')
    title = request.POST.get('title')
    author = request.POST.get('author')
    level = request.POST.get('level')
    hot_num = request.POST.get('hot_num')
    banner = request.FILES.get('banner')

    banner_name = ''
    if banner:
        banner_name = set_hash(banner.name)+'.'+banner.name.split('.')[-1]
        file_path = os.path.join(
            settings.BASE_DIR, 'app01/static/images/lol', banner_name)

        with open(file_path, 'ab') as f:
            for chunk in banner.chunks():
                f.write(chunk)

    mysql = DB(host='127.0.0.1',
               user='root',
               passwd='10011010',
               db='hgx_web')
    if banner:
        mysql.update(
            f'update tab_lol set title="{title}",author="{author}",level="{level}",hot_num="{hot_num}",banner="{banner_name}",addtime=now() where id="{id}"')
    else:
        mysql.update(
            f'update tab_lol set title="{title}",author="{author}",level="{level}",hot_num="{hot_num}",addtime=now() where id="{id}"')
    return redirect(f'/tips/?url=/list/&msg=修改成功')


def tips(request):
    msg = request.GET.get('msg', '操作成功')
    timer = request.GET.get('timer', 3)
    url = request.GET.get('url')
    result = {
        'msg': msg,
        'url': url,
        'timer': timer
    }
    return render(request, 'tips.html', {'result': result})


def sel_delete(request):
    id = request.GET.get('id')
    id = id[:-1]
    mysql = DB(host='127.0.0.1',
               user='root',
               passwd='10011010',
               db='hgx_web')
    mysql.delete(f'delete from tab_lol where id in ({id})')
    return HttpResponse('ok')


def add(request):
    return render(request, 'add.html')


def cate(request):
    return render(request, 'cate.html')
