import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Rating, Review

os.environ['DATABASE_URL'] = "postgresql:///myvideogamelist-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """ Create test client, add sample data """
        db.drop_all()
        db.create_all()

        u = User.register("test","password")
        uid = 1111
        u.id = uid

        db.session.commit()

        self.u = u
        self.uid = uid

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """Does user model work?"""

        u = User(username="testuser", password="HASHED_PASSWORD", email="testuser@test.com")

        db.session.add(u)
        db.session.commit()

        #User should have no ratings or reviews on creation

        self.assertEqual(len(u.ratings), 0)
        self.assertEqual(len(u.reviews), 0)


    ###### Sign Up Tests ######


    def test_valid_signup(self):
        u_test = User.register("testtest","password","test@testuser.com")
        uid = 1010
        u_test.id = uid
        db.session.commit

        u_test = User.query.get(uid)

        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username,"testtest")
        self.assertEqual(u_test.password, "password")
        self.assertEqual(u_test.email, "test@testuser.com")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.register(None,"password")
        uid = 2020
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        invalid = User.register("test",None)
        uid = 2019
        invalid.id = uid
        with self.assertRaises(ValueError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        invalid = User.register("test",'password',None)
        uid = 2018
        invalid.id = uid
        with self.assertRaises(ValueError) as context:
            db.session.commit()
    
    ##### Authenticate Tests #####

    def test_valid_authentication(self):
        u = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername","password"))
    
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u.username,"badpassword"))


