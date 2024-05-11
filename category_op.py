from flask import Flask , render_template,redirect,request
import mysql.connector

def showAllCategories():
    con = mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
    sql = "select * from category"
    cursor= con.cursor()
    cursor.execute(sql)
    result= cursor.fetchall()
    con.close()
    return render_template("showAllCategories.html", cats=result)

def addNewCategory():
    if request.method=="GET":
        return render_template("addNewCategory.html")
    else:
        cname=request.form["cname"]
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="insert into category (cname) values (%s)"
        val=(cname,)
        cursor= con.cursor()
        cursor.execute(sql,val)
        con.commit()
    return redirect("/showAllCategories")

def deleteCategory(cid):
    if request.method =="GET":
        return render_template("deleteConfirm.html")
    else:
        action =request.form["action"]
        if action == "Yes":
            con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
            sql="delete from category where cid=%s"
            val=(cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllCategories")
        
def editCategory(cid):
    if request.method == "GET":
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="select * from category where cid=%s"
        val=(cid,)
        cursor=con.cursor()
        cursor.execute(sql,val)
        result=cursor.fetchall()
        con.close()
        return render_template("editCategory.html", cat=result)
    else:
        cname=request.form["cname"]
        con=mysql.connector.connect(host="localhost", user="root", password="neha", database="bagshopdb")
        sql="update category set cname=%s where cid=%s"
        val=(cname,cid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCategories")