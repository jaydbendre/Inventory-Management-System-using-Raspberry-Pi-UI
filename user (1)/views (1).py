# Create your views here.
from django.shortcuts import render,redirect
import mysql.connector 
from django.contrib.auth import logout
from django.http import HttpResponse
from django.db import connection
import datetime
#import mypythoncode
#conn=mysql.connector.connect(host="localhost",database='inventory',user="root",password="hakunamatata")
#cursor=conn.cursor()

def index(request):
    return render(request, 'landing_index.html')

def admin(request):
    with connection.cursor() as cursor:
        data=dict()
        cursor.execute("SELECT * from user where uid= {} ".format(request.session["uid"]))
        result=cursor.fetchall()
        #return HttpResponse(result[0])
        data={
            "name": result[0][1],
            "dept": result[0][3],
            "email": result[0][4],
            "address": result[0][5]        
            } 
        sql="select m.m_id,p.name,m.in_lab,m.out_lab,m.user_id from movement as m , product as p  where p.rfid = m.p_id"
        cursor.execute(sql)
        res1=cursor.fetchall()
        #return HttpResponse(res1)
        data["table"]=res1
        data["table_len"]=len(res1) 
        return render(request, 'admin_index.html',data)
        #return render(request, 'admin_index.html')

def profile(request):
    request.session["uid"]=1
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from user where uid= {} ".format(request.session["uid"]))
        result=cursor.fetchall()
        #return HttpResponse(result[0])
        data={
            "name": result[0][1],
            "dept": result[0][3],
            "email": result[0][4],
            "address": result[0][5]        
            }
        if result[0][2]==0:
            data["role"]="Admin"
        elif result[0][2]==1:
            data["role"]="Lab Incharge"
        else:
            data["role"]="Clerk"
        # print(result)
        return render(request, 'admin_profile.html', data)


def check(request):
    #print (request.user.email)
    with connection.cursor() as cursor :
        sql= "select * from user where email= '{}' ".format(request.user.email) 
        # return HttpResponse(sql)
        #print(request.user.email)
        cursor.execute("select * from user where email='{}'".format(request.user.email))
        sql1 = cursor.fetchall()
        #print(sql1)
        if len(sql1) < 1:
            return HttpResponse("<h3>This is a test</h3>")
        else:
            login_in_user_cred = sql1[0]
            print(login_in_user_cred)
            data={
                "uid": login_in_user_cred[0],
                "name": login_in_user_cred[1],
                "role": login_in_user_cred[2],
                "dept": login_in_user_cred[3],
                "email": login_in_user_cred[4],
                "address":login_in_user_cred[5]
            }
            request.session["uid"]=data["uid"]
            request.session["username"]=data["name"]
            if data["role"] == 0:
                sql="select m.m_id,p.name,m.in_lab,m.out_lab,m.user_id from movement as m , product as p  where p.rfid = m.p_id"
                cursor.execute(sql)
                res1=cursor.fetchall()
                #return HttpResponse(res1)
                data["table"]=res1
                sql1="select req_id,pname,description from request where status = '{}'".format(0)
                cursor.execute(sql1)
                result=cursor.fetchall()
                data["info"]=result
                data["table_len"]=len(res1) 
                return render(request, 'admin_index.html',data)
            elif data["role"]== 1 :
                cursor.execute("SELECT number from labs where incharge_id={}".format(data["role"]))
                res=cursor.fetchall()
                print(res[0][0])
                cursor.execute("SELECT m.m_id,p.name,m.in_lab,m.out_lab,m.user_id from movement as m , product as p where (in_lab= {} or out_lab ={}) and p.rfid=m.p_id".format(res[0][0],res[0][0]))
                res=cursor.fetchall()
                print(res)
                data["table"]=res
                sql1="select * from request"
                cursor.execute(sql1)
                result=cursor.fetchall()
                data["info"]=result
                cursor.execute("select name from product")
                res1=cursor.fetchall()
                data["pname"]=res1
                return render(request,'lab_incharge.html',data)
            else:
                print("In else")
                sql="select m.m_id,p.name,m.in_lab,m.out_lab from movement as m , product as p  where m.user_id = {} and p.rfid = m.p_id order by m.m_id DESC".format(data["uid"])
                cursor.execute(sql)
                res1=cursor.fetchall()
                print(res1)
                data["table"]=res1
                data["table_len"]=len(res1)
                print(data)
                return render(request, 'clerk.html' ,data)
        #return HttpResponse(sql1)
        return render (request, 'landing_index.html')

def log_out(request):
    logout(request)
    return render(request,"landing_index.html")

def check_log(request):
    with connection.cursor() as cursor:
        cursor.execute("Select * from log")
        res=cursor.fetchall()
        return render(request,'test.html',{"res": res})

def lab_incharge(request):
    return render(request, "lab_incharge.html")

#def clerk(request):
    #return render(request, "clerk.html")

def movements(request):
    with connection.cursor() as cursor:
    # print("In else")
        cursor.execute("SELECT rfid_no,time FROM log order by log_id desc LIMIT 1")
        res=cursor.fetchall()
        #return HttpResponse(res[0][0])
        #sql="Select * from product where rfid = {} ".format(res[0])
        print("Test")
        sql="SELECT * FROM product WHERE rfid = {}".format(res[0][0])
        #return HttpResponse(sql)
        cursor.execute(sql)
        res1=cursor.fetchall()
        #return HttpResponse(res1)
        data=dict()
        if len(res1) == 0:
            data["error"]="No records Found for RFID TAG : {}".format(res[0][0])
            return render(request,'movement.html',data)
        else:
            print(res1)
            data={
                "rfid_no": res1[0][0],
                "name": res1[0][1],
                "details": res1[0][2],
                "source_lab": res1[0][3],
                "current_lab": res1[0][4],
                "last_serviced_date": res[0][1],
                "error": "",
                #"time": res[0][1]
            }
            #data[]
            #return HttpResponse(data["last_serviced_date"])
            request.session["rfid_to_update"]=data["rfid_no"]
            request.session["current_lab"]=data["current_lab"]
            #request.session["time"]=res[0][1]
            # data["table"]=res1
            # data["table_len"]=len(res1)
            # print(data)
            #return HttpResponse(data.items())
            return render(request,'movement.html',data)

def update_movement(request):
    option=request.POST.get("option")
    #return HttpResponse(sql)        
    if option != request.session["current_lab"]:
        with connection.cursor() as cursor : 
            cursor.execute("SELECT m_id from movement order by m_id DESC LIMIT 1")
            id=cursor.fetchall()[0][0]
            sql="INSERT INTO movement(m_id,p_id,in_lab,out_lab,user_id) values({},{},{},{},{})".format(str(id+1),request.session["rfid_to_update"],request.session["current_lab"],option,request.session["uid"])
            #return HttpResponse(sql)
            cursor.execute(sql)
            connection.commit()
            sql="UPDATE product set destination_lab= {}  where rfid= {} ".format(option,request.session["rfid_to_update"])
            cursor.execute(sql)
            connection.commit()       
            return redirect("/login_check")
            #return HttpResponse(sql)
    else:
        return HttpResponse("hi")

def admin_statistics(request):
    count=dict()
    lab_count=dict()
    hourly_count=dict()
    x=10
    with connection.cursor() as cursor:
        date_array=[]
        for i in range(10):
            date_array.append((datetime.date.today()- datetime.timedelta(days=10-i)))
        
        #return HttpResponse(i for i in date_array)
        #x= "SELECT count(*),start_date from movement where start_date <= '{}' and start_date > '{}' group by start_date ".format(datetime.date.today(),(datetime.date.today()- datetime.timedelta(days=10)).isoformat())
        #return HttpResponse(x)
        cursor.execute("SELECT count(*),start_date from movement where start_date <= '{}' and start_date > {} group by start_date ".format(datetime.date.today(),(datetime.date.today()- datetime.timedelta(days=10)).isoformat()))
        res=cursor.fetchall()
        j=0
        for i in date_array:
            count[j]={
                "date":i
            }
            f=0
            for y in res:
                #print(y,i)
                if i == y[1]:
                    #print(i)
                    f=1
                    count[j]["count"]=y[0]
                    break
            
            if f==0:
                count[j]["count"]=0
            
            j+=1
        #return HttpResponse(count.items())
        cursor.execute("SELECT count(*),in_lab from movement group by in_lab")
        res=cursor.fetchall()
        i=0
        for r in res:
            lab_count[i]={
                    "lab":r[1],
                    "count":r[0]
            }
            i+=1
        
        x=8
        for i in range(10):
            d=datetime.time(x+i,0,0)
            r=datetime.time(x+i+1,0,0)
            #return HttpResponse(d)
            cursor.execute("SELECT m_id,start_time from movement where start_time <= '{}' and start_time >= '{}' ".format(r,d))
            res=cursor.fetchall()
            hourly_count[i]={
                "count":len(res)
            }
        #return HttpResponse(str(lab_count.items())+str( count.items()))
        return render(request,"admin_statistics.html",{"count" : count, "lab_count":lab_count,"hourly_count":hourly_count })

def request_incharge(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            p_name=request.POST.get("product")
            description=request.POST.get("description")
            print(description)
            cursor.execute("insert into request(pname,description) values('{}','{}')".format(p_name,description))
    return redirect("/login_check")

def request_admin(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            accept = request.POST.get("accept")
            decline = request.POST.get("decline")
            arry = [accept,decline]
            #     "accept":accept,
            #     "decline":decline
            # }
            # if arry["accept"]
            # print(arry[0])
            # print(type(arry[0]))
            # print(type(arry[1]))
            if type(arry[0]) == str:
                print("accept")
                cursor.execute("update request set status = {0} where req_id = {1}".format(1,accept))
            elif type(arry[1]) == str:
                print("decline")
                cursor.execute("update request set status = {0} where req_id = {1}".format(2,decline))
            # if accept == '1':
                # print("test")
                # cursor.execute("update request set status = 1 where ")
            # elif decline == 2:
                # cursor.execute("update request set status = 2")
    return redirect("/login_check")
