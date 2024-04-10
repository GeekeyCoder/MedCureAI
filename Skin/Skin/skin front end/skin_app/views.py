from django.shortcuts import render, redirect
import shutil
import os
import easygui
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from skin_app import predict
import pandas  as pd

@csrf_exempt
def home(request):

   if request.method == "GET":
      return render(request,'signup.html')

@csrf_exempt
def submit(request):
   if request.method == "POST":
    image = request.FILES['image']
    shutil.rmtree(os.getcwd()+'\\static\\img')
    path = default_storage.save(os.getcwd()+'\\static\\img\\result.jpg', ContentFile(image.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    result = predict.process()
    result=result.split('/')
    f = open(os.path.dirname(__file__)+"/session.txt","r+")
    name = f.read()
    f.close()
    return render(request,'result.html',{"result":result[0],'name':name,'description':result[1]})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        print("inside signup")
        fullname = request.POST.get('fullname')
        print(fullname)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        cpass = request.POST.get('cpass')
        print(cpass)
        if password!= cpass:
            easygui.msgbox("The two password does not match", title="Error")
            return redirect('http://127.0.0.1:8000')
        else:
            print("inside database")
            file = open(os.path.dirname(__file__)+'/database.csv','a')
            file.write(fullname+","+email+","+password+"\n")
            file.close()
            print("done writing")
            # easygui.msgbox("Successfully registered", title="Success")
            return redirect('http://127.0.0.1:8000')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print("inside login")
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        flag = False

        with open(os.path.dirname(__file__)+'/database.csv','r') as file:
            for line in file:
                line = line.rstrip()
                line = line.split(",")
                print(line)
                if line[1] == email and line[2] == password:
                     f = open(os.path.dirname(__file__)+"/session.txt","w+")
                     f.write(line[0])
                     f.close()
                     flag = True

        if(flag):
            f = open(os.path.dirname(__file__)+"/session.txt","r+")
            name = f.read()
            f.close()
            return render(request, 'index.html',{"name":name})
        else:
            easygui.msgbox("Incorrect Username or password", title="Error")
            return redirect('http://127.0.0.1:8000')

@csrf_exempt
def logout(request):
   if request.method == 'GET':
      return redirect('http://127.0.0.1:8000')

@csrf_exempt
def dashboard(request):
   if request.method == 'GET':
       f = open(os.path.dirname(__file__)+"/session.txt","r+")
       name = f.read()
       f.close()
       return render(request,'index.html',{"name":name})
