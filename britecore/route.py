from flask import render_template, request, flash
from britecore import app, db
from britecore.quiz import quiz
from britecore import models
import string
import random
from sqlalchemy import func
from sqlalchemy import SQLAlchemyError


@app.route('/')
def index():
    clients = models.Client.query.all()
    areas = models.Productarea.query.all()
    return render_template('form.html', clients=clients, areas=areas)


@app.route('/requests')
def requests():
    clients = models.Client.query.all()
    areas = models.Productarea.query.all()
    reqs = models.Requests.query.all()
    return render_template('requests.html', clients=clients, areas=areas, reqs=reqs)


@app.route('/request/new', methods=['POST'])
def new_request():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        client = request.form['client']
        product_area = request.form['product_area']
        target_date = request.form['target_date']
        priority = request.form['level']
        pt = request.form.get('title')
        print(pt)
        if title and description and client and product_area and target_date and priority is not None:
            exist = models.Requests.query.filter(
                models.Requests.priority >= priority,
                models.Requests.client_id == client).all()
            for each in exist:
                each.priority = each.priority + 1
            prior = db.session.query(func.max(models.Requests.priority)).\
                filter(models.Requests.client_id == client).all()
            print(prior[0][0])

            if prior[0][0] is not None:
                if int(priority) <= int(prior[0][0]):
                    priority = int(prior[0][0]) + 1
            else:
                priority = priority
            print(priority)
            rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            req = models.Requests(rid=rand, title=title, description=description, client_id=client,
                                  product=product_area, target_date=target_date, priority=priority)
            exist.append(req)
            db.session.add_all(exist)
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                reason = str(e)
                flash(reason)
            if priority is not None:
                return "The feature request was submitted successfully"
        else:
            return 'Oops!!! All fields are required.'
    else:
        return 'Oops!!! Something went wrong', 'error'
