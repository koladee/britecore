import os
import unittest
from datetime import date
from britecore.models import Requests, Productarea, Client
from britecore import app, db



class Bucketlist(unittest.TestCase):
    """bucketlist test case"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        self.request = {
                        'rid': 'ho89hJHUHs',
                        'title': 'Request title',
                        'description': "The breakdown of request goes here",
                        'client_id': 1,
                        'product': 3,    
                        'target_date': '2018-11-06',
                        'priority': 4
                    }

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def create_client_and_request(self):
        client = Client(name="Test_client")
        data = [Requests(
            title=f'Request title {index+1}',
            description=f'The breakdown of request goes here {index+1}',
            client_id=1,
            product=1,    
            target_date=date(2019,03,23),
            priority=4
         ) for index, product in Productarea]
        data.append(client)
        db.session.add_all(data)
        db.session.commit()

    def create_new_request(self):
        res = self.client().post('/request/new', data=self.request)
        self.assertEqual(Requests.query.count(), 1)
        self.assertEqual(res.status_code, 302)

    def test_if_existing_requests are reorderd(self):
        self.create_client_and_request()
        self.assertEqual(Requests.query.count(), 4)
        self.assertEqual(Requests.query.get(1).title, 'title 1')
        self.assertEqual(Requests.query.get(1).priority, 1)
        res = self.client().post('/request/new', data=self.request)
        self.assertEqual(Requests.query.get(1).priority, 4)
        self.assertEqual(Requests.query.get(2).priority, 3)
        self.assertEqual(Requests.query.get(3).priority, 3)
        self.assertEqual(Requests.query.get(4).priority, 5)
        self.assertEqual(Requests.query.get(5).priority, 4)
        self.assertEqual(Requests.query.count(), 5)
        self.request.update(priority=3)
        res = self.client().post('/request/new', data=self.request)
        self.assertEqual(Requests.query.get(6).priority, 3)
        self.assertEqual(Requests.query.get(2).priority, 2)
        self.assertEqual(Requests.query.get(3).priority, 5)
        self.assertEqual(Requests.query.count(), 6)
        self.assertEqual(res.status_code, 302)

    def test_for_no_priority_duplicate(self):
        self.create_client_and_request()
        self.assertEqual(Requests.query.count(), 4)
        self.assertEqual(Requests.query.get(1).title, 'title 1')
        self.assertEqual(Requests.query.get(1).priority, 1)
        self.request.update({'priority':4})
        res = self.client().post('/request/new', data=self.request)
        self.assertEqual(Requests.query.get(1).priority, 1)
        self.assertEqual(Requests.query.get(2).priority, 2)
        self.assertEqual(Requests.query.get(3).priority, 3)
        self.assertEqual(Requests.query.get(4).priority, 5)
        self.assertEqual(Requests.query.get(5).priority, 4)
        self.assertEqual(Requests.query.count(), 5)
    
    def test_if_priority_of_requests_does_not_reordered_if_priority_on_new_request_is_not_set(self):
        self.create_client_and_request()
        self.assertEqual(Requests.query.count(), 4)
        self.assertEqual(Requests.query.get(1).title, 'title 1')
        self.assertEqual(Requests.query.get(1).priority, 1)
        self.request.update(priority=5)
        res = self.client().post('/request/new', data=self.request)
        self.assertEqual(Requests.query.get(1).priority, 1)
        self.assertEqual(Requests.query.get(2).priority, 2)
        self.assertEqual(Requests.query.get(3).priority, 3)
        self.assertEqual(Requests.query.get(4).priority, 4)
        self.assertEqual(Requests.query.get(5).priority, 5)
        self.assertEqual(Requests.query.count(), 5)
        self.assertEqual(res.status_code, 302)


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


