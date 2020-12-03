from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

from blog.models import Account

# Create your views here.
def index(request):
    return render(request, 'index.html')

#회원가입
class Signup(View):
    def post(self, request):
        data = request.POST
        if (data['password']==data['confirm']):
            user = User.objects.create_user(username=data['name'], email=data['email'], password=data['password'])
            return redirect('/')
        #password와 password confirm이 다름.
        return render(request, 'signup.html', {'error':'비밀번호가 틀립니다.'})

    def get(self, request):
        return render(request, 'signup.html')

#로그인
class Signin(View):
    def post(self, request):
        # 이메일 존재 여부 확인
        try:
            data = User.objects.filter(email=request.POST['email']).values()[0]
        except IndexError:
            return render(request, 'login.html', {'error':'회원정보 없음'})

        user = auth.authenticate(request, username=data.get('username'), password=request.POST['password'])
        # 입력한 비밀번호가 맞는지 확인
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        else:
             return render(request, 'login.html', {'error':'비밀번호 오류'})

    def get(self, request):
        return render(request, 'login.html')

#이메일 중복확인
def emailCheck(request, email):
    try:
        user = User.objects.filter(email=email).values()[0].get('email')
        jsonresult = {
            'result':'overlap'
        }
    except:
        jsonresult = {
            'result':'not overlap'
        }
        
    return JsonResponse(jsonresult) 