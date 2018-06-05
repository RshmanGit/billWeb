from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
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
        "login_fail": False,
        "errorflag": False,
        "newRegister": False,
    }
    return HttpResponse(html.render(context,request))

def errorIndex(request):
    html = loader.get_template("webapp/index.html")
    context = {
        "login_fail": False,
        "errorflag": True,
        "newRegister": False,
    }
    return HttpResponse(html.render(context, request))

def errorHome(request):
    try:
        if request.user:
            obtdData = obtainTodayData()
            html = loader.get_template("webapp/home.html")
            context = {
                "errorflag": True,
                "pendOrder": obtdData['pendOrder'],
                "todayRawMat": obtdData['todayRawMat'],
                "todayExps": obtdData['todayExps'],
                "username": request.user.username,
            }
            return HttpResponse(html.render(context, request))
        else:
            html = loginFail(request)
            return html
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html

def sucHome(request):
    try:
        if request.user:
            obtdData = obtainTodayData()
            html = loader.get_template("webapp/home.html")
            context = {
                "errorflag": False,
                "orderCompleted": True,
                "pendOrder": obtdData['pendOrder'],
                "todayRawMat": obtdData['todayRawMat'],
                "todayExps": obtdData['todayExps'],
                "username": request.user.username,
            }
            return HttpResponse(html.render(context, request))
        else:
            html = loginFail(request)
            return html
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html
    
def loginFail(request):
    html = loader.get_template("webapp/index.html")
    context = {
        "login_fail": True,
        "errorflag": False,
        "newRegister": False,
    }
    return HttpResponse(html.render(context, request))



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
            html = loginFail(request)
            return html
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html
    
def home(request):
    try:
        if request.user:
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
            html = loginFail(request)
            return html
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html
    
def register(request):
    try:
        html = loader.get_template("webapp/registerPage.html")
        context = {
            "errorflag": False,
        }
        return HttpResponse(html.render(context,request))
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html
    
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
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorIndex(request)
        return html
      
def insertOrder(request):
    try:
        html = loader.get_template("webapp/insertO.html")
        context = {
            "username": request.user.username,
        }
        return HttpResponse(html.render(context, request))
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def insertOrderReq(request):
    try:
        URL = "http://localhost:4000/api/v1/order/"
        
        orderId = int(request.POST['id'])
        Id = (orderId * 10000) + (date.today().year)
        custname = request.POST['custname']
        prodname = request.POST['prodname']
        phonenumb = request.POST['phnumber']
        village = request.POST['village']
        quantity = request.POST['quantity']
        d_date = request.POST['ddate']
        o_date = date.today()
        
        
        DATA = {
            "delivery_date": str(d_date),
            "id": Id,
            "customer_name": custname,
            "product_name": prodname,
            "mobile_number": phonenumb,
            "order_date": str(o_date),
            "quant_delivered": 0,
            "quantity": quantity,
            "village": village,
        }
        
        HEADERS = {
            "Content-Type": "application/json",
        }
        
        DATA = json.dumps(DATA, default=json_util.default)
        
        print(DATA)
        
        r = requests.post(url = URL, data = DATA, headers = HEADERS)
        
        ret = home(request)
        return ret
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    

def insertRawMat(request):
    try:
        html = loader.get_template("webapp/insertR.html")
        context = {
            "username": request.user.username,
        }
        return HttpResponse(html.render(context, request))
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
        
def insertRawMatReq(request):
    try:
        URL = "http://localhost:4000/api/v1/rawMat/"
        
        gate = int(request.POST['gatepass'])
        gatepass = (gate * 10000) + (date.today().year)
        name = request.POST['name']
        desc = request.POST['desc']
        weight = request.POST['weight']
        o_date = date.today()
        
        DATA = {
            "gatePass": gatepass,
            "name": name,
            "desc": desc,
            "order_date": str(o_date),
            "weight": weight,
        }
        
        DATA = json.dumps(DATA, default=json_util.default)
        
        HEADERS = {
            "Content-Type": "application/json",
        }
        
        r = requests.post(url = URL, data = DATA, headers = HEADERS)
        
        ret = home(request)
        return ret
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def insertExps(request):
    try:
        html = loader.get_template("webapp/insertE.html")
        context = {
            "username": request.user.username,
        }
        return HttpResponse(html.render(context, request))
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def insertExpsReq(request):
    try:
        URL = "http://localhost:4000/api/v1/exps/"
        
        desc = request.POST['desc']
        cost = request.POST['cost']
        cashInHand = request.POST['cashinhand']
        o_date = date.today()
        
        DATA = {
            "desc": desc,
            "cost": cost,
            "date": str(o_date),
            "cashInHand": cashInHand,
        }
    
        DATA = json.dumps(DATA, default=json_util.default)
        
        HEADERS = {
            "Content-Type": "application/json",
        }
        
        r = requests.post(url = URL, data = DATA, headers = HEADERS)
        
        ret = home(request)
        
        return ret
    
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
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
    
def fullorderscall():
    try:
        URL = "http://localhost:4000/api/v1/order/"
        data = []
        PARAMS = {}
        temp = requests.get(url = URL, params = PARAMS)
        temp = temp.json()
        for obj in temp['objects']:
            data = [obj] + data
        
        return data
        
    except Exception as e:
        return False
    
def fullorders(request):
    try:
        data = []
        data = fullorderscall()
        context = {
            "username": request.user.username,
            "orderdata": data,
        }
        html = loader.get_template("webapp/fullorder.html")
        return HttpResponse(html.render(context, request))        
        
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def fullrawmatscall():
    try:
        URL = "http://localhost:4000/api/v1/rawMat/"
        data = []
        PARAMS = {}
        temp = requests.get(url = URL, params = PARAMS)
        temp = temp.json()
        for obj in temp['objects']:
            data = [obj] + data
        
        return data
        
    except Exception as e:
        return False
    
def fullrawmat(request):
    try:
        data = []
        data = fullrawmatscall()
        context = {
            "username": request.user.username,
            "rawmatdata": data,
        }
        html = loader.get_template("webapp/fullrawmat.html")
        return HttpResponse(html.render(context, request))        
        
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def fullexpscall():
    try:
        URL = "http://localhost:4000/api/v1/exps/"
        data = []
        PARAMS = {}
        temp = requests.get(url = URL, params = PARAMS)
        temp = temp.json()
        for obj in temp['objects']:
            data = [obj] + data
        
        return data
        
    except Exception as e:
        return False
    
def fullexps(request):
    try:
        data = []
        data = fullexpscall()
        context = {
            "username": request.user.username,
            "expsdata": data,
        }
        html = loader.get_template("webapp/fullexps.html")
        return HttpResponse(html.render(context, request))        
        
        
    except Exception as e:
        print('[-] '+str(e))
        html = errorHome(request)
        return html
    
def logoutreq(request):
    logout(request)
    html = loader.get_template("webapp/index.html")
    context = {}
    return HttpResponse(html.render(context, request))

def getOrder(Id):
    URL = "http://localhost:4000/api/v1/order/" + str(Id)
    data = []
    PARAMS = {}
    temp = requests.get(url = URL, params = PARAMS)
    temp = temp.json()
    
    return temp

def updateOrder(request,Id):
    
    order = getOrder(Id)
    html = loader.get_template("webapp/updateOrder.html")
    context = {
        "order": order,
    }
    
    return HttpResponse(html.render(context, request))

def updateOrderReq(request,Id):
    try:
        URL = "http://localhost:4000/api/v1/order/"
        
        order = getOrder(Id)
        
        orderId = order['id']
        custname = order['customer_name']
        prodname = request.POST['prodname']
        phnumb = request.POST['phnumber']
        village = order['village']
        quantity = request.POST['quantity']
        quant_delivered = request.POST['quantity_delivered']
        d_date = request.POST['ddate']
        o_date = order['order_date']
        
        delivered = True
        
        if(quant_delivered < quantity):
            delivered = False
            
        DATA = {
            "delivery_date": str(d_date),
            "id": orderId,
            "customer_name": custname,
            "product_name": prodname,
            "mobile_number": phnumb,
            "order_date": str(o_date),
            "quant_delivered": quant_delivered,
            "quantity": quantity,
            "village": village,
            "delivered": delivered,
        }
        
        HEADERS = {
            "Content-Type": "application/json",
        }
        
        DATA = json.dumps(DATA, default=json_util.default)
        
        print(DATA)
        r = requests.post(url = URL, data = DATA, headers = HEADERS)
        
        ret = sucHome(request)
        return ret
    except Exception as e:
        print(e)
        html = errorHome(request)
        return HttpResponse(html)
    
def getRawMat(gatePass):
    URL = "http://localhost:4000/api/v1/rawMat/" + str(gatePass)
    data = []
    PARAMS = {}
    temp = requests.get(url = URL, params = PARAMS)
    temp = temp.json()
    
    return temp

def updateRawMat(request,gatePass):
    
    rawMat = getRawMat(gatePass)
    html = loader.get_template("webapp/updateRawMat.html")
    context = {
        "rawMat": rawMat,
    }
    
    return HttpResponse(html.render(context, request))

def updateRawMatReq(request, gatePass):
    
    try:
        URL = "http://localhost:4000/api/v1/rawMat/"
        
        rawMat = getRawMat(gatePass)
        
        gatePassr = rawMat['gatePass']
        name = rawMat['name']
        desc = request.POST['desc']
        o_date = request.POST['odate']
        weight = request.POST['weight']
        
        DATA = {
            "gatePass": gatePassr,
            "name": name,
            "desc": desc,
            "order_date": o_date,
            "weight": weight,
        }
        
        HEADERS = {
            "Content-Type": "application/json",
        }
        
        DATA = json.dumps(DATA, default=json_util.default)
        
        print(DATA)
        r = requests.post(url = URL, data = DATA, headers = HEADERS)
        
        ret = home(request)
        return ret
    except Exception as e:
        print(e)
        html = errorHome(request)
        return HttpResponse(html)