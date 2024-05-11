from flask import Flask,render_template,redirect,request,session,url_for
import mysql.connector
from datetime import datetime
from flask_mail import Mail,Message




def homePage():
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    sql="select * from bag"
    cursor=con.cursor()
    cursor.execute(sql)
    bags=cursor.fetchall()
    sql="select * from category"
    cursor=con.cursor()
    cursor.execute(sql)
    cats=cursor.fetchall()
    con.close()
    return render_template("homepage.html", bags=bags, cats=cats)

def showBags(cid):
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    sql="select * from bag where cat_id=%s"
    val=(cid,)
    cursor=con.cursor()
    cursor.execute(sql,val)
    bags=cursor.fetchall()
    sql="select * from category"
    cursor=con.cursor()
    cursor.execute(sql)
    cats=cursor.fetchall()
    con.close()
    return render_template("homepage.html", bags=bags, cats=cats)

def viewDetails(bagid):
    con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
    sql = "select * from bag where bagid=%s"
    val = (bagid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    bag = cursor.fetchone()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("viewDetails.html",bag = bag,cats=cats)

def search():
    bag_name = request.form['search_name']
    if not bag_name:
        return redirect(url_for('/'))
    
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    sql= "select * from bag where bag_name = %s"
    val=(bag_name,)
    cursor=con.cursor()
    cursor.execute(sql,val)
    bags=cursor.fetchall()
    con.close()
    
    return render_template("search.html", bags=bags)
    
      

def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname=request.form["uname"]
        pwd=request.form["pwd"]
        sql="select count(*) from UserInfo where username=%s and password=%s and role='user'"
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        val=(uname,pwd)
        cursor=con.cursor()
        cursor.execute(sql,val)
        result=cursor.fetchone()
        con.close()
        if (int(result[0])==1):
            session["uname"]=uname
            return redirect("/")
        else:
            msg='Incorect credentials !'
    return render_template("login.html", msg=msg)
        
def checkDuplicate(uname):
    sql="select count(*) from UserInfo where username=%s and role='user'"
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    val=(uname,)
    cursor=con.cursor()
    cursor.execute(sql,val)
    result=cursor.fetchone()
    con.close()
    if int(result[0])==1:
        return True
    else:
        return False
    
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        uname = request.form["uname"]        
        pwd=request.form["pwd"]
        email=request.form["email"]
        result=checkDuplicate(uname)
        if(result):
            return render_template("signup.html", message="User Already Exits. Plase use different username.")
        else:
            sql="insert into UserInfo values (%s,%s,%s,'user')"
            con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
            val=(uname,pwd,email)
            cursor=con.cursor()
            cursor.execute(sql,val)
            con.commit()
            con.close()
            return redirect("/")
        
def logout():
    session.clear()
    return redirect("/")

def addToCart():
    con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
    cursor = con.cursor()
    if "uname" in session:
        uname = session["uname"]
        bagid=request.form["bagid"]
        qty = request.form["qty"]
        sql="select count(*) from mycart where username=%s and bag_id=%s"
        val=(uname,bagid)
        cursor.execute(sql,val)
        bag=cursor.fetchone()[0]
        if(int(bag)>=1):
            msg='Item already in cart'
            return render_template("viewDetails.html",bag=bag, msg=msg)
        else:
            sql = "insert into mycart (username,bag_id,qty) values (%s,%s,%s)"
            val = (uname,bagid,qty)
            cursor.execute(sql,val)
            con.commit()
        con.close()  
        return redirect("/")        
    else:
        return redirect("/login")
    
def showCart():
    con= mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    cursor = con.cursor()
    if request.method == "GET":
        sql="select * from mycart_vw where username=%s"
        val = (session["uname"],)
        cursor.execute(sql,val)
        result=cursor.fetchall()
        sql="select sum(subtotal) from mycart_vw where username=%s"
        val=(session["uname"],)
        cursor.execute(sql,val)
        sum = cursor.fetchone()[0]
        session["total"]=sum
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("showCart.html",bags=result,sum=sum, cats=cats)
    else:
        action=request.form["action"]
        bagid=request.form["bagid"]
        uname= session["uname"]
        if (action=="delete"):
            sql="delete from mycart where bag_id=%s and username=%s"
            val=(bagid,uname)
        elif (action=="update"):
            qty=request.form["qty"]
            sql="update mycart set qty=%s where bag_id=%s and username=%s"
            val=(qty,bagid,uname)
        
        cursor.execute(sql,val)
        con.commit()
        con.close()
        return redirect(url_for("showCart"))


def makePayment():
    if request.method=="GET":
        return render_template("makePayment.html")
    else:
        uname=request.form["uname"]
        cardno=request.form["cardno"]
        cvv=request.form["cvv"]
        expiry=request.form["expiry"]
        sql="select count(*) from mypayment where uname=%s and cardno=%s and cvv=%s and expiry=%s"
        val=(uname,cardno,cvv,expiry)
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        cursor=con.cursor()
        cursor.execute(sql,val)
        data=cursor.fetchone()
        if int(data[0]) == 1:
            sql = "select balance from mypayment where uname=%s and cardno=%s and cvv=%s and expiry=%s"
            val = (uname,cardno,cvv,expiry)
            con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
            cursor = con.cursor()
            cursor.execute(sql,val)
            data = cursor.fetchone()
            if float(data[0] < session["total"]):
                message = "Insufficent balance"                
                return redirect(url_for("makePayment",message=message))
            else:
                buyer="update mypayment set balance= balance - %s where cardno=%s and cvv =%s"
                owner="update mypayment set balance= balance + %s where cardno=444 and cvv=444"
                val1=(session["total"], cardno,cvv)
                val2=(session["total"],)
                cursor.execute(buyer,val1)
                cursor.execute(owner,val2)
                con.commit()
                updateOrderMaster()
                return redirect("/")
        else:
            return redirect(url_for("makePayment"))
        
def sendConfirmationEmail():
    message = Message( 
                'Conformation', 
                sender ='nehakinjalkar@gmail.com', 
                recipients = ['nehakinjalkar@gmail.com'] 
               ) 
    message.body = 'your order is conformed'
    Mail.send(message) 
    return 'sent'


def updateOrderMaster():
    uname=session["uname"]
    sql="select bag_id,qty from mycart where username=%s"
    val=(uname,)
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    cursor=con.cursor()
    cursor.execute(sql,val)
    result=cursor.fetchall()
    data=[]
    for bag in result:
        bag = str(bag[0])+ "," + str(bag[1])
        data.append(bag)
    data = "|".join(data)
    sql = " insert into orderMaster(username,description, date_of_order,amount) values (%s,%s,%s,%s)"
    dd= datetime.now().strftime("%y-%m-%d")
    val=(uname,data,dd,session["total"])
    cursor.execute(sql,val)
    con.commit()


    # update cake table
    for bag in result:
        sql="update bag set quantity=quantity -%s where bagid=%s"
        val= (bag[1],bag[0])
        cursor.execute(sql,val)
    con.commit()
    sql="delete from mycart where username= %s"
    val=(session["uname"],)
    cursor.execute(sql,val)
    con.commit()

def myorders():
    con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
    sql="select * from ordermaster"
    cursor=con.cursor()
    cursor.execute(sql)
    orders=cursor.fetchall()
    con.close()
    return render_template("view_orders.html",orders=orders)

    

def Wishlist(bagid):
    con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
    sql = "select * from bag where bagid=%s"
    val = (bagid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    bag = cursor.fetchone()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("Wishlist.html",bag = bag,cats=cats)

def addToWishlist():
    con = mysql.connector.connect(host="localhost",user="root",password="neha",database="bagshopdb")
    cursor = con.cursor()
    if "uname" in session:
        uname = session["uname"]
        bagid=request.form["bagid"]
        qty = request.form["qty"]
        sql = "insert into wishlist (username,bag_id,qty) values (%s,%s,%s)"
        val = (uname,bagid,qty)
        
        cursor.execute(sql,val)
        con.commit()
        con.close()  
        return redirect("/")        
    else:
        return redirect("/login")
    
def showWishlist():
    con= mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    cursor = con.cursor()
    if request.method == "GET":
        sql="select * from wishlist_view where username=%s"
        val = (session["uname"],)
        cursor.execute(sql,val)
        result=cursor.fetchall()
        sql="select sum(subtotal) from wishlist_view where username=%s"
        val=(session["uname"],)
        cursor.execute(sql,val)
        sum = cursor.fetchone()[0]
        session["total"]=sum
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("showWishlist.html",bags=result,sum=sum, cats=cats)
    else:
        action=request.form["action"]
        bagid=request.form["bagid"]
        uname= session["uname"]
        if (action=="delete"):
            sql="delete from wishlist where bag_id=%s and username=%s"
            val=(bagid,uname)
        elif (action=="update"):
            qty=request.form["qty"]
            sql="update wishlist set qty=%s where bag_id=%s and username=%s"
            val=(qty,bagid,uname)
        else:
            uname = session["uname"]
            bagid=request.form["bagid"]
            qty = request.form["qty"]
            sql = "insert into mycart (username,bag_id,qty) values (%s,%s,%s)"
            val = (uname,bagid,qty)
        cursor.execute(sql,val)
        con.commit()
        con.close()
        return redirect(url_for("showWishlist"))


def send_email():
    if request.method == 'POST':
        recipient_email = request.form['recipient_email']
        subject = request.form['subject']
        message_body = request.form['message_body']

        # Create a message
        message = Message(subject=subject, recipients=[recipient_email], body=message_body)

        # Send the email
        Mail.send(message)

        return redirect(url_for('/'))