 # -*- coding: utf-8 -*-
from app import app, db, transmit
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, SatCoord, AntCoord, Angels
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, BD_coordinates
from werkzeug.urls import url_parse
import json
from datetime import datetime

coordinates = transmit.Coordinates()


@app.route('/')
@app.route('/index')
@login_required
def index():
	posts = []
	return render_template('index.html', title = 'Home', posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # собирает все данные, запускает все валидаторы, прикрепленные к полям, и если все в порядке, вернет True

        user = User.query.filter_by(username=form.username.data).first() # ищет пользователя в бд
        if user is None or not user.check_password(form.password.data): # проверяет соответствие введенного пароля и имеющегося в бд
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data) # запоминает вошедшего пользователя, если стоит галка запомнить
        next_page = request.args.get('next') # получаем значение next-аргумента строки запроса
        if not next_page or url_parse(next_page).netloc != '': # проверка на принадлежность next-аргумента данному приложению
            next_page = url_for('index')
        return redirect(next_page) # перенаправляет пользователя на /index


    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/ant_coord', methods=['GET', 'POST'])
def ant_coord():
    ant_form = AntCoord()
    
    if ant_form.validate_on_submit(): 
        coordinates.ant_lat = ant_form.ant_lat.data
        coordinates.ant_long = ant_form.ant_long.data
        coordinates.ant_height = ant_form.ant_height.data
        return redirect(url_for('sat_coord'))
    else:
        ant_form.ant_lat.data = coordinates.ant_lat
        ant_form.ant_long.data = coordinates.ant_long
        ant_form.ant_height.data = coordinates.ant_height
    
    return render_template('ant_coord.html', ant_form=ant_form) 

@app.route('/sat_coord', methods=['GET', 'POST'])
def sat_coord():
    sat_form = SatCoord()
    teta, fi_priv = 0, 0

    if sat_form.validate_on_submit(): 
        coordinates.sat_lat = sat_form.sat_lat.data
        coordinates.sat_long = sat_form.sat_long.data
        coordinates.sat_height = sat_form.sat_height.data
        teta, fi_priv = coordinates.transmit()
        bd_coordinates = BD_coordinates(sat_lat=sat_form.sat_lat.data, 
                                        sat_long=sat_form.sat_long.data,
                                        sat_height=sat_form.sat_height.data,
                                        ant_lat=coordinates.ant_lat,
                                        ant_long=coordinates.ant_long,
                                        ant_height=coordinates.ant_height,
                                        teta=int( teta ),
                                        fi_priv=int( fi_priv ),
                                        timestamp = datetime.now())
        db.session.add(bd_coordinates)
        db.session.commit()

        # управление вращением
        lora = transmit.PublicLora(teta, fi_priv)



        return redirect(url_for('maps'))
    else:
        sat_form.sat_lat.data = coordinates.sat_lat
        sat_form.sat_long.data = coordinates.sat_long
        sat_form.sat_height.data = coordinates.sat_height


        

    return render_template('sat_coord.html', sat_form=sat_form)

@app.route('/sat_coord_json', methods=['GET', 'POST'])
def sat_coord_json():
    sat_form = SatCoord()
    teta, fi_priv = 0, 0


    coordinates.sat_lat = sat_form.sat_lat.data
    coordinates.sat_long = sat_form.sat_long.data
    coordinates.sat_height = sat_form.sat_height.data
    teta, fi_priv = coordinates.transmit()
    bd_coordinates = BD_coordinates(sat_lat=sat_form.sat_lat.data, 
                                    sat_long=sat_form.sat_long.data,
                                    sat_height=sat_form.sat_height.data,
                                    ant_lat=coordinates.ant_lat,
                                    ant_long=coordinates.ant_long,
                                    ant_height=coordinates.ant_height,
                                    teta=teta,
                                    fi_priv=fi_priv,
                                    timestamp = datetime.now())
    db.session.add(bd_coordinates)
    db.session.commit()
    return json.dumps({'teta' : int(teta), 'fi_priv' : int(fi_priv)})
    
@app.route('/log', methods=['GET', 'POST'])
def log():
    logs = BD_coordinates.query.all()

    #print( logs )

    return render_template('log.html', logs=logs)

@app.route( '/maps' )
def maps():
    return render_template( 'maps.html',  sat_lat = coordinates.sat_lat, sat_long = coordinates.sat_long, ant_lat = coordinates.ant_lat, ant_long =coordinates.ant_long)


@app.route( '/angels' , methods=['GET', 'POST'])
def angels():

    angel = Angels()

    if angel.validate_on_submit(): 

        teta, fi_priv = angel.teta.data, angel.fi_priv.data
        lora = transmit.PublicLora(teta, fi_priv)

    return render_template('angels.html', angel = angel)








