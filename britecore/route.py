from flask import render_template, request, flash
from britecore import app, db
from britecore import models
import string
import random
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError


def process_request(ob):
    title = ob['title']
    description = ob['description']
    client = ob['client']
    product_area = ob['product_area']
    target_date = ob['target_date']
    priority = ob['level']
    if title and description and client and product_area and target_date and priority is not None:
        exist = models.Requests.query.filter(
            models.Requests.priority >= priority,
            models.Requests.client_id == client).all()
        for each in exist:
            if int(priority) == int(each.priority):
                prior = db.session.query(func.max(models.Requests.priority)). \
                    filter(models.Requests.client_id == client).all()
                each.priority = int(prior[0][0]) + 1
            else:
                print(each.priority)
                each.priority = each.priority

        rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        req = models.Requests(rid=rand, title=title, description=description, client_id=client,
                              product=product_area, target_date=target_date, priority=priority)
        exist.append(req)
        db.session.add_all(exist)
        done = False
        try:
            db.session.commit()
            done = True
        except SQLAlchemyError as e:
            reason = str(e)
            flash(reason)
        return done
    else:
        return 'Oops!!! All fields are required.'

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
        forms = request.form
        done = process_request(forms)
        if done is True:
            return "The feature request was submitted successfully"
        else:
            return "Oops! An error occurred while trying to process your request."
    else:
        return 'Oops!!! Something went wrong', 'error'
