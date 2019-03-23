import os
import json
import unittest
from datetime import date

from request import app, db, models
from request.models import Request, Client, ProductEnum
from config.settings import basedir


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        self.request = {
                        'title': 'title 1',
                        'description': "description 2",
                        'client': 1,
                        'priority': 1,
                        'target_date': '2018-11-06',
                        'product': 'claims'    
                    }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def create_test_client_and_request(self):
        client = Client(name="client A")
        data = [Request(
            title=f'title {index+1}',
            description=f'description {index+1}',
            client_id=1,
            priority=index+1,
            target_date=date(2018,11,6),
            product=product    
         ) for index, product in enumerate(ProductEnum)]
        data.append(client)
        db.session.add_all(data)
        db.session.commit()

    def test_request_creation(self):
        res = self.client().post('/', data=self.request)
        self.assertEqual(Request.query.count(), 1)
        self.assertEqual(res.status_code, 302)

    def test_requests_gets_reordered_if_priority_on_new_request_is_already_set(self):
        self.create_test_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        res = self.client().post('/', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 2)
        self.assertEqual(Request.query.get(2).priority, 3)
        self.assertEqual(Request.query.get(3).priority, 4)
        self.assertEqual(Request.query.get(4).priority, 5)
        self.assertEqual(Request.query.get(5).priority, 1)
        self.assertEqual(Request.query.count(), 5)
        self.request.update(priority=3)
        res = self.client().post('/', data=self.request)
        self.assertEqual(Request.query.get(6).priority, 3)
        self.assertEqual(Request.query.get(2).priority, 4)
        self.assertEqual(Request.query.get(3).priority, 5)
        self.assertEqual(Request.query.count(), 6)
        self.assertEqual(res.status_code, 302)

    def test_no_duplicate_if_priority_on_new_request_is_equal_to_all_request_count(self):
        self.create_test_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        self.request.update({'priority':4})
        res = self.client().post('/', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 1)
        self.assertEqual(Request.query.get(2).priority, 2)
        self.assertEqual(Request.query.get(3).priority, 3)
        self.assertEqual(Request.query.get(4).priority, 5)
        self.assertEqual(Request.query.get(5).priority, 4)
        self.assertEqual(Request.query.count(), 5)
    
    def test_requests_does_not_reordered_if_priority_on_new_request_is_not_set(self):
        self.create_test_client_and_request()
        self.assertEqual(Request.query.count(), 4)
        self.assertEqual(Request.query.get(1).title, 'title 1')
        self.assertEqual(Request.query.get(1).priority, 1)
        self.request.update(priority=5)
        res = self.client().post('/', data=self.request)
        self.assertEqual(Request.query.get(1).priority, 1)
        self.assertEqual(Request.query.get(2).priority, 2)
        self.assertEqual(Request.query.get(3).priority, 3)
        self.assertEqual(Request.query.get(4).priority, 4)
        self.assertEqual(Request.query.get(5).priority, 5)
        self.assertEqual(Request.query.count(), 5)
        self.assertEqual(res.status_code, 302)


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


