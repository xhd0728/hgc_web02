from django.shortcuts import render, redirect

# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('code')
    if username == 'admin' and password == '123456' and code == '6982':
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
    return render(request, 'list.html')


def add(request):
    return render(request, 'add.html')


def cate(request):
    return render(request, 'cate.html')
