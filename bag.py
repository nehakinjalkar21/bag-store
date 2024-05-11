from flask import Flask,render_template,redirect,request,url_for
import mysql.connector
from werkzeug.utils import secure_filename

def showAllBags():
    con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    sql="select b.bagid, b.bag_name, b.price, b.description, b.img_url, b.quantity, t.cname from bag b inner join category t on b.cat_id=t.cid"
    cursor= con.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    con.close()
    return render_template("showAllbags.html",bags=result)

def addNewBag():
    if request.method=="GET":
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        con.close()
        return render_template("addNewBags.html", cats=result)
    else:
        cname=request.form["cname"]
        price=request.form["price"]
        desc=request.form["desc"]
        qty=request.form["qty"]
        cid=request.form["cat"]
        f=request.files["img_url"]
        filename=secure_filename(f.filename)
        filename="static/Images/" + f.filename
        f.save(filename)
        filename="Images/" +f.filename
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql= "insert into bag (bag_name,price,description,img_url,quantity,cat_id) values (%s,%s,%s,%s,%s,%s)"
        val=(cname,price,desc,filename,qty,cid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllBags"))

def deleteBags(bagid):
    if request.method=="GET":
        return render_template("deleteConfirm.html")
    else:
        action=request.form["action"]
        if action=="Yes":
            con=mysql.connector.connect(host="localhost",user="root", password="neha", database="bagshopdb")
            sql="delete from bag where bagid=%s"
            val=(bagid,)
            cursor=con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllBags")
    
def editBags(bagid):
    if request.method=="GET":
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="select * from bag where bagid=%s"
        val=(bagid,)
        cursor=con.cursor()
        cursor.execute(sql,val)
        bag= cursor.fetchone()

        sql="select * from category"
        cursor=con.cursor()
        cursor.execute(sql)
        cats= cursor.fetchall()
        con.close()
        return render_template("editBags.html", bag=bag,cats=cats)
    else:
        cname=request.form["cname"]
        price=request.form["price"]
        desc=request.form["desc"]
        qty=request.form["qty"]
        cid=request.form["cat"]
        f=request.files["img_url"]
        filename=secure_filename(f.filename)
        filename="static/Images/" + f.filename
        f.save(filename)
        filename="Images/" +f.filename
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="update bag set bag_name=%s, price=%s, description=%s, img_url=%s, quantity=%s, cat_id=%s where bagid=%s"
        val=(cname,price,desc,filename,qty,cid, bagid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllBags"))        
