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
        return redirect(f'/index/?user={username}')
    return redirect('/login/')


def index(request):
    username = request.GET.get('username')
    return render(request, 'index.html', {'username': username})


def info(request):
    return render(request, 'info.html')


def update_pwd(request):
    username = request.GET.get('username')
    return render(request, 'pass.html', {'username': username})


def handle_pwd(request):
    username = request.POST.get('username')
    old_pwd = request.POST.get('old_pwd')
    new_pwd = request.POST.get('new_pwd')
    renew_pwd = request.POST.get('renew_pwd')
    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
    password = mysql.findone(
        f'select password from tab_user where username = "{username}"')['password']
    if password != old_pwd:
        return redirect(f'/tips/?url=/list/&msg=旧密码输入错误')
    if new_pwd != renew_pwd:
        return redirect(f'/tips/?url=/list/&msg=两次密码输入不一致')
    mysql.update(
        f'update tab_user set password = "{new_pwd}" where username = "{username}"')
    return redirect(f'/tips/?url=/list/&msg=修改成功')


def page(request):
    return render(request, 'page.html')


def adv(request):
    return render(request, 'adv.html')


def book(request):
    return render(request, 'book.html')


def column(request):
    return render(request, 'column.html')


def list_(request):
    mysql = DB(host='127.0.0.1',  user='root', passwd='10011010', db='hgx_web')
    sub_sql = ''
    search_type = request.GET.get('search_type')
    keyword = request.GET.get('keyword')
    if search_type != '':
        if search_type == '1':
            sub_sql = f'where author like "%{keyword}%"'
        elif search_type == '2':
            sub_sql = f'where level like "%{keyword}%"'
    page = int(request.GET.get('page', 1))
    total_count = len(mysql.findall(f'select id from tab_lol {sub_sql}'))
    page_size = 10
    start = (page-1)*page_size
    res_list = mysql.findall(
        f'select * from tab_lol {sub_sql} order by num asc limit {start},{page_size}')
    if search_type != '':
        page_string = handle_page(
            page, total_count, page_size, search_type=search_type, keyword=keyword)
    else:
        page_string = handle_page(page, total_count, page_size)
    return render(request, 'list.html', {'res_list': res_list, 'page_string': page_string, 'search_type': search_type, 'keyword': keyword})


def handle_delete(request):
    id = request.GET.get('id')
    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
    mysql.delete(
        f'delete from tab_lol where id = "{id}"')
    return redirect('/list/')


def show_update(request):
    id = request.GET.get('id')
    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
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

    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
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
    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
    mysql.delete(f'delete from tab_lol where id in ({id})')
    return HttpResponse('ok')


def update_num(request):
    id = request.GET.get('id')
    value = request.GET.get('value')
    mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
    mysql.update(f'update tab_lol set num = "{value}" where id = "{id}"')
    return HttpResponse('ok')


def add(request):
    return render(request, 'add.html')


def cate(request):
    return render(request, 'cate.html')
