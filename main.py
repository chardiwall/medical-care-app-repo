# developed by: Samiulhaq Chardiwall
# LinkedIn: https://www.linkedin.com/in/chardiwall/
# start time: 20/july/2022

# Document Name: __init__.py
# Application Name: Medical Care Final Year Project


# ----------- General libraries -------------------
import os
import json
import numpy as np
from PIL import Image

# ----------- Email sending libraries -------------------
import smtplib

# ----------- Deep learning specific libraries -------------------
import tensorflow as tf

# ----------- Visulization specific libraries -------------------
import plotly
import plotly.express as px

# ----------- Flask specific libraries -------------------
from flask import make_response, redirect, render_template
from flask import Blueprint, request, flash


main = Blueprint('main', __name__)


# home page
@main.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            # reading user image
            image =  request.files['img']
            print(image)
            # resizing and normalizing the image for predicting
            image = Image.open(image).resize((100, 100))
            image = np.array(image).astype('float32')/255
            image = np.expand_dims(image, axis=0)

            # loading model and making prediction
            model = tf.keras.models.load_model('Xception_Model.h5')
            pred=model.predict(image)[0]

            # lession types
            lesion_type_cat = [
                'Melanocytic nevi (nv)',
                'Melanoma (mel)',
                'Actinic keratosis (ak)',
                'Benign keratosis-like lesions (bkl)',
                'Basal cell carcinoma (bcc)',
                'Vascular lesions (vasc)',
                'Squamous cell carcinoma (SCC) ',
                'Dermatofibroma (df)',
            ]

            #finding the class of predicted image
            predicted_class_ind = np.argmax(pred)
            pred = pred.tolist()
            print(pred)

            predicted_class = lesion_type_cat[predicted_class_ind]

            # short form of the skin cancer categories
            lesion_type_cat_short = ['nv', 'mel', 'ak', 'bkl', 'bcc', 'vasc', 'scc', 'df']
            
            # creating plotly bar graph
            fig = px.pie(names=lesion_type_cat, values=pred, color=lesion_type_cat)
            fig.update_yaxes(range=[0,1])
            fig.update_layout(title_text='Model confidintiality', title_x=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')

            # dumping bar graph in jason to send to fron end
            figGraph = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

            # redirecting to result page
            res = make_response(render_template('result.html', 
                                    figGraph = figGraph,
                                    predicted_class = predicted_class,
                                    user = request.cookies.get('user')
                                    )
            )

            return res
    except Exception as e:
        print(e) 

    return render_template('index.html', user = request.cookies.get('user'))


# ----------- About Page Management -------------------
@main.route('/about')
def about():
    return render_template('about.html', user = request.cookies.get('user'))

@main.route('/result')
def result():
    return render_template('result.html', user = request.cookies.get('user'))



# ----------- Contact us Page Managment -------------------
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    try:

        if not request.cookies.get('user'):
            # redirecting to login page
                response = make_response(redirect('/login'))
                flash("You need to be logged in before using this page!", 'warning')
                return response

        if request.method == 'POST':
            
            # reading name and email of user from cookies
            user = request.cookies.get('user')
            user_email = request.cookies.get('email')

            # reading subject and the message of user
            subject = request.form.get('subject')
            msg = request.form.get('msg')

            # making connection to gmail server using smtp library
            connection = smtplib.SMTP('smtp.gmail.com')
            
            # adding trasport layer security
            connection.starttls()

            # retrieving gmail and its password from env file for sending emails
            admin_mail = os.environ.get('GMAIL')
            password = os.environ.get('PASSWORD')
            print(admin_mail, password)

            connection.login(user=admin_mail, password=password)

            msg_tobe_send =f'''\n
--- Massage From Medical Care App --- \n\n\n
User Name: {user} \n
User Email: {user_email}   \n\n
Subject: {subject} \n
Massage: {msg}
'''

            connection.sendmail(from_addr=admin_mail,
                                to_addrs=admin_mail,
                                msg=msg_tobe_send)

            
            connection.close()

            flash('We Have Recieved Your Message. Thank You!', 'success')
    except Exception as e:
        flash(e, 'danger')

    return render_template('contact.html', user = request.cookies.get('user'))


@main.route('/profile')
def profile():
    pass