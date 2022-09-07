# developed by: Samiulhaq Chardiwall, Usama Khawreen
# LinkedIn: https://www.linkedin.com/in/chardiwall/
# start time: 19/july/2022
# end time: 25/july/2022

# Document Name: auth.py
# for: auth/base.html
# Application Name: Medical Care Final Year Project


# ----------- Flask specific libraries -------------------
from flask import make_response
from flask import render_template
from flask import Blueprint, flash, redirect, request


# ----------- Email sending libraries -------------------
import smtplib

# Firebase
# ----------- Firebase specific libraries -------------------
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth as authen


# ----------- General  libraries -------------------
import os
import re
import json
import requests
import webbrowser
from random import randint
from dotenv import load_dotenv


# ------------------------------------- AUTH Module -----------------------------------

auth = Blueprint('auth', __name__)

load_dotenv()  # take environment variables from .env.

# ------------------------------------- AUTH Module -----------------------------------

# connecting to firebase
cred = credentials.Certificate('serviceAccount.json')
defaultApp = firebase_admin.initialize_app(cred)


# Checking whether email exist or not
def isEmail(aut, email):
    try:
        # if email does not exists in the database an errror will be arised
        aut.get_user_by_email(email)
        return False
    except:
        return True



# ------------- user login management ------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # email pattern validation
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    

    # retriving user cookies
    if request.cookies.get('user'):
        return redirect('/')

    if request.method == 'POST':
        try:
            # retriving data from form fields
            email = request.form['email']
            password = request.form['password']
            
            # email Validation
            if len(email) == 0:
                raise Exception('Email is Required!')
            
            elif not re.fullmatch(regex, email):
                raise Exception('Invalid Email!\n Email Should be of shape someone@gmail.com!')
            
            # user login using rest api
            else:
                aut = authen.Client(defaultApp)
                if isEmail(aut, email):
                    raise Exception('Email Does Not Exists!')
                
                # retriving api key form .env file
                FIREBASE_WEB_API_KEY = os.environ["FIREBASE_WEB_API_KEY"]

                #-------------- user login using rest api ----------

                # creating connection with google api
                rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

                # storing email and password in json variable
                payload=json.dumps({
                    'email': email,
                    'password': password,
                    'return_secure_token': False
                })
                
                # requesting user login
                res = requests.post(rest_api_url, 
                                    params={"key": FIREBASE_WEB_API_KEY},
                                    data=payload).json()
                if res.get('error'):
                    raise Exception(res['error']['message'])

                # setting user cookies and redirecting to home page
                user = res.get('displayName', 'USER')
                res =  make_response(redirect('/'))
                res.set_cookie('user', user)
                res.set_cookie('email', email)
                return res

        except Exception as e:
            flash(e, 'danger')

    return render_template('auth/login.html')


# -------------------- sign up management -----------------------
@auth.route('/signup', methods = ['GET', 'POST'])
async def signup():
    # email pattern validation
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    name_regex = r'\b[A-Za-z]{2,}\b'

    if request.method == 'POST':
        try:
            # retriving data from form fields
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']

            # user Name Validation
            if not re.fullmatch(name_regex, first_name):
                raise Exception('First Name Accepts only Alphbatic words A-z and should be atleast 2 character long!')
            
            if not re.fullmatch(name_regex, last_name):
                raise Exception('Last Name Accepts only Alphbatic words A-z and should be atleast 2 character long!')
            
            # user email  Validation
            if len(email) == 0:
                raise Exception('Email is Required!')
            
            elif not re.fullmatch(email_regex, email):
                raise Exception('Invalid Email! Email Should be of shape someone@gmail.com')

            # user password Validation
            if len(password) == 0:
                raise Exception('Password is Required!')
            
            elif len(password) < 6:
                raise Exception('Password must be atleast 6 charactes!')
            
            # signing up user using firebase
            else:
                aut = authen.Client(defaultApp)
                # check email first
                if not isEmail(aut, email):
                    raise Exception('Email Already Exists!')
                
                # creating user with provided email and password and full name
                full_name = first_name + ' ' + last_name
                aut.create_user(email=email, password=password, display_name=full_name)

                # showing  success messages and redirecting to login page
                flash('You are registered and can login now!', 'success')
                return redirect ('/login')
        
        except Exception as e:
            flash(e, 'danger')

    return render_template('auth/signup.html')


# email password reset management
@auth.route('/reset-password', methods=['GET', 'POST'])
def reset():
    # creating authentication object
    aut = authen.Client(defaultApp)
    try:
        if request.method == 'POST':
            # retrievin email
            email = request.form['email']

            # checking user email if it exist or not!
            aut = authen.Client(defaultApp)
            if isEmail(aut, email):
                raise Exception('Email Does Not Exists!')


            # retrieving gmail and its password from env file for sending emails
            admin_mail = os.environ.get('GMAIL')
            password = os.environ.get('PASSWORD')

            #genrating otp code
            otp = randint(1000, 9999)

            # making connection to gmail server using smtp library
            connection = smtplib.SMTP('smtp.gmail.com')
            
            # adding trasport layer security
            connection.starttls()

            # login admin for sending emails
            connection.login(user=admin_mail, password=password)

            msg_tobe_send =f'''\n
   --- Massage From Medical Care App --- \n\n\n
Your OTP Code is  {otp}  do not share this code with others. \n
'''
            # sending otp code in email
            connection.sendmail(from_addr=admin_mail,
                                to_addrs=email,
                                msg=msg_tobe_send)
            # closing smpt connection
            connection.close()
            response = make_response(redirect('/confirmOTP'))
            response.set_cookie('rand_num', str(otp*759246))
            response.set_cookie('email', email)
            return response

    except Exception as e:
        flash(e, 'danger')

    # rediricting to generated link
    return render_template('auth/reset-password.html')

@auth.route('/confirmOTP', methods=['GET', 'POST'])
def confermOTP():
    # retrieving OTP code
    try:
        if request.method == 'POST':
            # retrieving OTP code
            otp = request.form['otp']

            # creating authentication object
            aut = authen.Client(defaultApp)

            if int(otp) != int(request.cookies.get('rand_num'))/759246:
                raise Exception('Incorrect OTP code')
            # generating and rendering reset link
            link = aut.generate_password_reset_link(request.cookies.get('email'))
            webbrowser.open_new_tab(link)

            response = make_response(redirect('/login'))
            response.set_cookie('rand_num', expires=0)
            return response

    except Exception as e:
        flash(e, 'danger')

    # rediricting to generated link
    return render_template('auth/otpConfirmation.html')


# --------- logout user managment ------------------------------
@auth.route('/logout', methods=['GET', 'POST'])
def session_logout():

    # redirecting to login page
    response = make_response(redirect('/login'))

    # clearing cookies
    response.set_cookie('session', expires=0)
    response.set_cookie('user', expires=0)
    response.set_cookie('email', expires=0)

    flash('You have logged out! Thanks for stoping by', 'info')
    return response 