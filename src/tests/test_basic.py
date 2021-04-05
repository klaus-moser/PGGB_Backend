import unittest

from create_app import create_app
from src.db import db


class BaseCase(unittest.TestCase):
    """
    This is the base class for all test-classes.
    """
    def setUp(self):
        self.app = create_app(mode='TEST').test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.reflect()
        self.db.drop_all()
