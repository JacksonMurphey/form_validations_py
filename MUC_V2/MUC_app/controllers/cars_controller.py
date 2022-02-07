from MUC_app import app
from flask import render_template, redirect, request
from MUC_app.models.car import Car
from MUC_app.models.user import User
from MUC_app.models.maker import Maker

#we will user this for login and registration/possibly move this to user.py
@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/cars')
def car_dashboard():
    cars = Car.get_all()
    return render_template('cars_dash.html', cars=cars)


@app.route('/cars/new')
def car_new():
    users = User.get_all()
    makers = Maker.get_all()
    return render_template('cars_new.html', makers=makers, users=users)


@app.route('/cars/create', methods=['POST'])
def car_create():
    if not Car.validate(request.form):
        return redirect('/cars/new')
    data = {
        'color' : request.form['color'],
        'year' : request.form['year'],
        'user_id' : request.form['user_id'],
        'maker_id' : request.form['maker_id'],
    }
    Car.save(data)
    return redirect('/cars')


@app.route('/cars/<int:car_id>')
def car_show(car_id):

    data = {
        'id' : car_id,
    }
    # car = Car.get_one(data)
    # car = Car.get_one_with_maker(data) 
    # car = Car.get_one_with_user(data) 
    #NOTE here we are had car = to one method, that method only joined one table. thus, our html only is displaying either the user or the maker data. to fix this, we will create another method called: get_one_complete(), name doesnt matter. the point however is to join both user and maker tables, so we can display all the data. 
    car = Car.get_one_complete(data)
    return render_template('cars_show.html', car=car)


@app.route('/cars/<int:car_id>/edit')
def car_edit(car_id):

    # get one car
    data = {
        'id' : car_id,
    }
    # populate a form
    car = Car.get_one(data)
    # update the car
    return render_template('cars_edit.html', car=car)


@app.route('/cars/<int:car_id>/update', methods=['POST'])
def car_update(car_id):

    #validating inputs in form are correct
    if not Car.validate(request.form):
        return redirect(f'/cars/{car_id}/edit')
    #update the car
    data = {
        'id': car_id,
        'color': request.form['color'],
        'year': request.form['year'],
    }
    Car.update(data)
    return redirect(f'/cars/{car_id}') #when using REDIRECT we will need to use F-Strings


@app.route('/cars/<int:car_id>/destroy')
def car_destroy(car_id):
    data = {
        'id': car_id,
    }
    Car.delete(data)
    return redirect('/cars')
