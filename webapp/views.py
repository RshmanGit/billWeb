from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import date
import requests
from bson import json_util
import json

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
            obtdData = obtainTodayData()
            login(request, user)
            html = loader.get_template("webapp/home.html")
            context = {
                "pendOrder": obtdData['pendOrder'],
                "todayRawMat": obtdData['todayRawMat'],
                "todayExps": obtdData['todayExps'],
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
    except Exception as e:
        html = loader.get_template("webapp/index.html")
        login_fail = False
        errorflag = True
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        print(e)
        return HttpResponse(html.render(context, request))
    
def home(request):
    try:
        if request.user is not None:
            obtdData = obtainTodayData()
            html = loader.get_template("webapp/home.html")
            context = {
                "pendOrder": obtdData['pendOrder'],
                "todayRawMat": obtdData['todayRawMat'],
                "todayExps": obtdData['todayExps'],
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
    except Exception as e:
        html = loader.get_template("webapp/index.html")
        errorflag = True
        login_fail = False
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        print(e)
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
    
def obtainTodayData():
    try:
        data = {}
        data['pendOrder'] = []
        data['todayRawMat'] = []
        data['todayExps'] = []
        URL = "http://localhost:4000/api/v1/"
        keys = ['pendOrder','todayRawMat','todayExps']
        for i in keys:
            PARAMS = {}
            temp = requests.get(url = URL+i, params = PARAMS)
            temp = temp.json()
            templist = []
            for obj in temp['objects']:
                templist.append(obj)
            data[i] = templist
            
        return data
        
    except:
        return False
    
def insertOrder(request):
    try:
        html = loader.get_template("webapp/insertO.html")
        context = {
            "username": request.user.username,
        }
        return HttpResponse(html.render(context, request))
    
    except Exception as e:
        print(e)
        html = loader.get_template("webapp/index.html")
        context = {
            "login_fail": login_fail,
            "errorflag": errorflag,
            "newRegister": False,
        }
        return HttpResponse(html.render(context, request))
    
def insertOrderReq(request):
    try:
        URL = "http://localhost:4000/api/v1/order/"
        
        orderId = int(request.POST['id'])
        Id = (orderId * 10000) + (date.today().year)
        name = request.POST['name']
        village = request.POST['village']
        quantity = request.POST['quantity']
        d_date = request.POST['ddate']
        o_date = date.today()
        
        DATA = {
            "delivery_date": str(d_date),
            "id": Id,
            "name": name,
            "order_date": str(o_date),
            "quant_delivered": 0,
            "quantity": quantity,
            "village": village
        }
        
        DATA = json.dumps(DATA, default=json_util.default)
        
        print(DATA)
        
        r = requests.post(url = URL, data = DATA)
        
        ret = home(request)
        return ret
        
    except Exception as e:
        print('[-] '+str(e))
        html = loader.get_template("webapp/index.html")
        context = {
            "login_fail": False,
            "errorflag": True,
            "newRegister": False,
        }
        return HttpResponse(html.render(context, request))