import unittest
from app.models.blacklist import Blacklist
from app import create_app, db


class LoanTest(unittest.TestCase):
    """Test API"""

    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)

    def test_create_loan(self):
        """Test creating loan"""
        result = self.client.post('/api/loan/', json=dict(amount=5000, term="2024-01-01", first_name="first", last_name="last", personal_id=111))

        self.assertEqual(result.status_code, 201)
        self.assertIn('2024-01-01', str(result.data))

    def test_create_loan_timed_out(self):
        """Test creating too many applications in 24 hours"""
        self.client.post('/api/loan/', json=dict(amount=1000, term="2024-01-01", first_name="first", last_name="last", personal_id=111))
        self.client.post('/api/loan/', json=dict(amount=2000, term="2025-01-01", first_name="first", last_name="last", personal_id=111))
        self.client.post('/api/loan/', json=dict(amount=3000, term="2026-01-01", first_name="first", last_name="last", personal_id=111))
        result = self.client.post('/api/loan/', json=dict(amount=4000, term="2027-01-01", first_name="first", last_name="last", personal_id=111))

        self.assertEqual(result.status_code, 200)
        self.assertIn('Too many applications in 24 hours', str(result.data))

    def test_create_loan_blacklisted(self):
        """Test creating application when blacklisted"""
        with self.app.app_context():
            db.session.add(Blacklist(personal_id=444))
            db.session.commit()

        result = self.client.post('/api/loan/', json=dict(amount=4000, term="2024-01-01", first_name="first", last_name="last", personal_id=444))

        self.assertEqual(result.status_code, 200)
        self.assertIn('User is blacklisted', str(result.data))

    def test_get_loans_by_borrower(self):
        """Test getting all loans by borrower"""
        self.client.post('/api/loan/', json=dict(amount=1000, term="2024-01-01", first_name="first", last_name="last", personal_id=111))
        self.client.post('/api/loan/', json=dict(amount=2000, term="2025-01-01", first_name="new", last_name="user", personal_id=222))
        self.client.post('/api/loan/', json=dict(amount=3000, term="2026-01-01", first_name="first", last_name="last", personal_id=111))

        result = self.client.get('/api/loan/1')

        self.assertEqual(result.status_code, 200)
        self.assertIn('1000', str(result.data))
        self.assertIn('2026-01-01', str(result.data))
        self.assertIsNot('2025-01-01', str(result.data))


if __name__ == "__main__":
    unittest.main()
