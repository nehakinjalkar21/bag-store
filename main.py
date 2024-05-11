from flask import Flask,render_template, redirect, request,Response
from flask_msearch import Search
from flask_mail import Mail,Message


app=Flask(__name__)
app.secret_key="firstbit"
mail = Mail(app)


from urls import *



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nehakinjalkar@gmail.com'
app.config['MAIL_PASSWORD'] = 'madhukar12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)


if __name__== "__main__":
    app.run(debug=True)
    