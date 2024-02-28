from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, authenticate, login
import uuid
import base64
import redis
import json
from core.models import CustomUser
import ghasedakpack

def encode_base64(data):
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def generate_random_code():
    import random
    return str(random.randint(10000000, 99999999))

# Create your views here.
def login(request):
    email = ''
    if request.method == 'POST':
        try:
            email_address = request.POST.get('email')
            user = CustomUser.objects.get(email=email_address)
        except Exception:
            return render(request, 'accounts/login.html',context={'email':email,'alert':"کاربری با این ایمیل ثبت نشده است"})    
        redis_conn = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        if request.POST.get('send_otp_code') == 'pso':
            sms = ghasedakpack.Ghasedak("9de30ff2c771cb47c8e969d4663b6d408e0b186d00c8e82200f4d5817f88d2c8")
            otp_code = generate_random_code()
            otp_code_enc = encode_base64(otp_code)
            redis_key = f"login:{email_address}"
            data_to_store = {'user_id': user.id, 'otp_code': otp_code_enc}
            redis_conn.set(redis_key, json.dumps(data_to_store))
            redis_conn.expire(redis_key, 300)
            
            # sms.verification({'receptor': str(user.phone),'type': '1','template': 'PerfumeSite','param1': str(otp_code)})
            print('sms sent', otp_code)
            email = email_address
            return render(request, 'accounts/login.html',context={'email':email,'s_alert':"پیام با موفقیت ارسال شد"})
            
        elif request.POST.get('password') != '':
            password = request.POST.get('password')
            if check_password(password, user.password):
                user_token = str(uuid.uuid4())  
                user.token = user_token
                user.is_active = True
                user.save()
                print(user.password)
                response = redirect('home') 
                response.set_cookie('login_token', user_token, max_age=10000)
                return response
            
            else:
                return render(request, 'accounts/login.html',context={'email':email,'alert':"رمز عبور وارد شده صحیح نمیباشد"})    
                
        else:
            otp_code = request.POST.get('otp_code')
            redis_key = f"login:{email_address}"
            stored_data = redis_conn.get(redis_key)
            
            if stored_data:
                stored_data = json.loads(stored_data)
                user_id = stored_data.get('user_id')
                orginal_otp_code = decode_base64(stored_data.get('otp_code'))
                
                if otp_code == orginal_otp_code:
                    user_token = str(uuid.uuid4()) 
                    user.token = user_token
                    user.is_active = True
                    user.save()
                    response = redirect('home') 
                    response.set_cookie('login_token', user_token, max_age=10000) 
                    redis_key = f"login:{email_address}"
                    data_to_store = {}
                    redis_conn.set(redis_key, json.dumps(data_to_store))
                    return response
                
                else:
                    return render(request, 'accounts/login.html',context={'email':email,'alert':"کد وارد شده صحیح نمیباشد"})    
                
            else:
                return render(request, 'accounts/login.html',context={'email':email,'alert':"برای این کاربر کدی ثبت نشده"})
    return render(request, 'accounts/login.html',context={'email':email})

def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        if name == '' or lastname == '' or email == '' or tel == '' or password == '':
            return render(request, 'accounts/signup.html',context={'name':name,'lastname':lastname,'email':email,'phone':tel,'alert':"لطفا تمام موارد را وارد کنید"})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html',context={'name':name,'lastname':lastname,'email':email,'phone':tel,'alert':"این ایمیل قبلا ثبت شده است"})
        if CustomUser.objects.filter(phone=tel).exists():
            return render(request, 'accounts/signup.html',context={'name':name,'lastname':lastname,'email':email,'phone':tel,'alert':"این شماره تماس قبلا ثبت شده است"})
        
        user_token = str(uuid.uuid4())  
        user = get_user_model().objects.create_user(
            first_name=name,
            last_name=lastname,
            email=email,
            phone=tel,
            password=password,
            token=user_token,
            role='customer',
        )
        user.is_active = True
        user.save()
        response = redirect('home') 
        response.set_cookie('login_token', user_token, max_age=10000)
        return response

    return render(request, 'accounts/signup.html', context={})

def profile(request):
    return render(request, 'accounts/profile.html', context={})
