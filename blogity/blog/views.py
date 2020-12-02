from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User

from blog.models import Account

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

#회원가입
class Signup(View):
    def post(self, request):
        data = request.POST
        Account.objects.create(
            name = data['name'],
            email = data['email'],
            password = data['password']
        )
        User.objects.create_user(username=data['name'], email=data['email'], password=data['password'])
        return redirect('/')

    def get(self, request):
        return render(request, 'signup.html')

#로그인
class Signin(View):
    def post(self, request):
        data = request.POST
        print(data)
        return redirect('/')