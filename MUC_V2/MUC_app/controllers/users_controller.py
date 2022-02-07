from MUC_app import app
from flask import render_template, redirect, request
from MUC_app.models.user import User

@app.route('/users')
def user_dashboard():
    users = User.get_all()
    return render_template('users_dash.html', users=users)

@app.route('/users/new')
def user_new():
    return render_template('users_new.html')

@app.route('/users/create', methods=['POST'])
def user_create():
    if not User.validate(request.form):
        return redirect('/users/new')
    User.save(request.form)
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_show_complete(user_id):
    data = {
        'id' : user_id,
    }
    # user = User.get_one(data)
    # user = User.get_one_with_maker(data) 
    # user = User.get_one_with_user(data) 
    
    user = User.get_one_complete(data)
    return render_template('users_show.html', user=user)

@app.route('/users/<int:user_id>')
def user_show(user_id):
    data = {
        'id': user_id,
    }
    user = User.get_one(data)
    return render_template('users_show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    data = {
        'id': user_id,
    }
    user = User.get_one(data)
    return render_template('users_edit.html', user=user)

@app.route('/users/<int:user_id>/update', methods=['POST'])
def user_update(user_id):
    if not User.validate(request.form):
        return redirect(f'/users/{user_id}/edit')
    data = {
        'id': user_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    User.update(data)
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/destroy')
def user_destroy(user_id):
    data = {
        'id': user_id,
    }
    User.delete(data)
    return redirect('/users')
    