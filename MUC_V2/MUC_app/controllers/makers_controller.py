from MUC_app import app
from flask import render_template, redirect, request
from MUC_app.models.maker import Maker

@app.route('/makers')
def maker_dashboard():
    makers = Maker.get_all()
    return render_template('makers_dash.html', makers=makers)

@app.route('/makers/new')
def maker_new():
    return render_template('makers_new.html')

@app.route('/makers/create', methods=['POST'])
def maker_create():
    if not Maker.validate(request.form):
        return redirect(f'/makers/new')
    Maker.save(request.form)
    return redirect('/makers')

@app.route('/makers/<int:maker_id>')
def maker_show(maker_id):
    data = {
        'id': maker_id,
    }
    maker = Maker.get_one(data)
    return render_template('makers_show.html', maker=maker)

@app.route('/makers/<int:maker_id>/edit')
def maker_edit(maker_id):
    
    data = {
        'id': maker_id,
    }
    maker = Maker.get_one(data)
    return render_template('makers_edit.html', maker=maker)

@app.route('/makers/<int:maker_id>/update', methods=['POST'])
def maker_update(maker_id):
    if not Maker.validate(request.form):
        return redirect(f'/makers/{maker_id}/edit')
    data = {
        'id': maker_id,
        'name': request.form['name'],
    }
    Maker.update(data)
    return redirect(f'/makers/{maker_id}')

@app.route('/makers/<int:maker_id>/destroy')
def maker_destroy(maker_id):
    data = {
        'id': maker_id,
    }
    Maker.delete(data)
    return redirect('/makers')