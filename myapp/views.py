from django.shortcuts import render,redirect
from django.http import HttpResponse
#from zmq import device
from .models import LongToShort
from .models import Meta_Data
import json
import requests

# Create your views here.
def hello_world(request):
    return HttpResponse("HELLO WORLD") 


def home_page(request):
    
    context_data={
        "submitted": False,
        "error": False
    }
    if(request.method=='POST'):
        
        data=request.POST
        longurl=data['long_url']
        customname=data['custom_name']
        
    
        try:
            obj=LongToShort(long_url=longurl,short_url=customname)
            obj.save()
            context_data["submitted"]=True
            context_data["date"]=obj.date
            context_data["clicks"]=obj.clicks
        except:
            context_data["error"]=True
            
        context_data["long_url"]=longurl
        context_data["short_url"]= request.build_absolute_uri()+customname
        
    else:
        print("NO data found")
        
    return render(request,"index.html",context_data)


def redirect_url(request,short_url):
    print(short_url)
    row=LongToShort.objects.filter(short_url=short_url)
    if len(row)==0:
        return HttpResponse("NO such url exist")
    obj=row[0]
    long_url=obj.long_url

    obj.clicks=obj.clicks+1
    obj.save()



    #new code
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    device_type = ""
    browser_type = ""
    os_type = ""
    
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    browser_type = request.user_agent.browser.family
    os_type = request.user_agent.os.family
    context_metadata = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "os_type":os_type,
    }
    string1="http://api.ipstack.com/"
    string2="?access_key=1081db7f9542e3cca739358ce1b4ee3f"
    link=string1+ip+string2
    

    resp = requests.get(link)
    data = resp.json()
    countryname=data["country_name"]
    if(countryname==None):
        countryname="Unites States"
    
    #countryname="China"
    #data["country_name"]=countryname
    print(data)
    print(data["country_code"])
    meta_obj=Meta_Data(new_short_url=short_url,country_name=countryname,device_name=device_type,browser_name=browser_type)
    meta_obj.save()
    # print(meta_obj)
    #code end
    
    
    # #print(request.META)
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    # #return ip
    # string1="http://api.ipstack.com/"
    # string2="?access_key=1081db7f9542e3cca739358ce1b4ee3f"
    # link=string1+ip+string2
    # # print(link)
    # resp = requests.get(link)
    # data = resp.json()
    # meta_obj=Meta_Data(country_name=data.country_name,device_name="Laptop",browser_name="Google")
    # meta_obj.save()

    
    return redirect(long_url)
    
def all_analytics(request):
    rows=LongToShort.objects.all()
    new_context={
        "rows":rows
    }
    
    return render(request,"all-analytics.html",new_context)
    


def url_analytics(request,short_urls):
    print(short_urls)
    row=Meta_Data.objects.filter(new_short_url=short_urls)
    row_url=LongToShort.objects.filter(short_url=short_urls)
    obj_temp=row_url[0]
    n=len(row)
    
    url_dict={
        "short_url":short_urls,
        "long_url":obj_temp.long_url,
        "clicks":obj_temp.clicks,
        "last_visit":row[n-1].last_visit
    }
    print(url_dict["last_visit"])
    url_dict["date"]=obj_temp.date
    country_dict={}
    browser_dict={}
    device_dict={}
    #device_dict[ele.device_name]=device_dict[ele.device_name]+1
    set1=set()
    for ele in row:
       cn=ele.country_name
       if(cn=="United State"):
        cn="USA"
       if(cn=="United Kingdom"):
        cn="UK"
       dn=ele.device_name
       bn=ele.browser_name
       set1.add(cn)
       url_dict[cn] = url_dict.get(cn, 0) + 1
       url_dict[dn]=url_dict.get(dn,0)+1
       url_dict[bn]=url_dict.get(bn,0)+1
    
    
    list1=list(set1)
    url_dict["country_list"]=list1
    
    
    return render(request,"analytics.html",url_dict)
    
def test(request):
    
    context_data={
        "name":"bhushan"
    }
    return render(request,"test.html",context_data)