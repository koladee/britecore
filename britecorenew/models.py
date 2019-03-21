from britecorenew import db
import enum
from datetime import datetime


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    requests = db.relationship('Requests', backref='client', lazy=True)

    def __repr__(self):
        return f"<Client(name='{self.name}')>"


class Productarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    request = db.relationship('Requests', backref='productarea', lazy=True)

    def __repr__(self):
        return f"<Product(name='{self.name}')>"


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    rid = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('productarea.id'), nullable=False)
    target_date = db.Column(db.String(12), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Request(client='{self.client}', title='{self.title}', priority='{self.priority}')>"
