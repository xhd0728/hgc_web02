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
