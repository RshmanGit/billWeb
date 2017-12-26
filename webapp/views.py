from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

login_fail = False
errorflag = False

# Create your views here.
#@csrf_exempt
def loginreq(request):
    html = loader.get_template("webapp/index.html")
    context = {
        "login_fail": login_fail,
        "errorflag": errorflag,
        "newRegister": False,
    }
    return HttpResponse(html.render(context,request))

def autho(request):
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            html = loader.get_template("webapp/home.html")
            context = {
                "username": user.username,
            }
            return HttpResponse(html.render(context, request))
        else:
            html = loader.get_template("webapp/index.html")
            login_fail = True
            errorflag = False
            context = {
                "login_fail": login_fail,
                "errorflag": errorflag,
                "newRegister": False,
            }
            return HttpResponse(html.render(context, request))
    except:
        html = loader.get_template("webapp/index.html")
        login_fail = False
        errorflag = True
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        return HttpResponse(html.render(context, request))
    
def home(request):
    try:
        if request.user is not None:
            html = loader.get_template("webapp/home.html")
            context = {
                "username": request.user.username,
            }
            return HttpResponse(html.render(context, request))
        else:
            html = loader.get_template("webapp/index.html")
            login_fail = True
            errorflag = False
            context = {
                "login_fail": login_fail,
                "errorflag": errorflag,
                "newRegister": False,
            }
            return HttpResponse(html.render(context, request))
    except:
        html = loader.get_template("webapp/index.html")
        errorflag = True
        login_fail = False
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        return HttpResponse(html.render(context, request))
    
def register(request):
    try:
        html = loader.get_template("webapp/registerPage.html")
        context = {
            "errorflag": False,
        }
        return HttpResponse(html.render(context,request))
    except:
        html = loader.get_template("webapp/index.html")
        errorflag = True
        login_fail = False
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        return HttpResponse(html.render(context,request))
    
def registerReq(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username,'',password)
        user.save()
        html = loader.get_template("webapp/index.html")
        context = {
            "newRegister": True,
        }
        return HttpResponse(html.render(context,request))
    except:
        html = loader.get_template("webapp/registerPage.html")
        context = {
            "errorflag": True,
        }
        return HttpResponse(html.render(context,request))