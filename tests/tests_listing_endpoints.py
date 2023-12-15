import unittest
from app import app

class TestListingsEndpoints(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_all_listings_success(self):
        response = self.client.get('/listings')
        self.assertEqual(response.status_code, 200)  

    def test_get_listing_by_id_success(self):
        response = self.client.get('/listings/1')  # Replace '1' with a valid listing ID
        self.assertEqual(response.status_code, 200)  # Check for a successful request

    def test_get_listing_by_id_failure(self):
        response = self.client.get('/listings/999')  # Using a non-existing ID to simulate failure
        self.assertEqual(response.status_code, 404)  # Check for a failure (listing not found)

    def test_create_listing_success(self):
        data = {
            'name': 'New Listing',
            'price': 100,
            'description': 'A beautiful new listing'
        }
        response = self.client.post('/listings', json=data)
        self.assertEqual(response.status_code, 201)  # Check for successful creation

    def test_create_listing_failure(self):
        data = {
            'availability_365': 306,
            'host_id': 8028,
            'host_name': 'Sylvia'
        }
        response = self.client.post('/listings', json=data)
        self.assertEqual(response.status_code, 400)  # Check for a failure (invalid request)

    def test_search_listings_success(self):
        data = {
            'search_terms': '2 bedroom'  # Provide a valid search term
        }
        response = self.client.post('/listing/search', json=data)
        self.assertEqual(response.status_code, 200)  # Check for a successful search

    def test_search_listings_failure(self):
        data = {
            'search_terms': ''
        }
        response = self.client.post('/listing/search', json=data)
        self.assertEqual(response.status_code, 400)  # Check for a failure (invalid search)

    def test_update_listing_success(self):
        listing_id = 5456  # Replace with an existing listing ID
        data = {
            'price':200,
            'name':"loki's house"
        }
        response = self.client.patch(f'/listings/{listing_id}', json=data)
        self.assertEqual(response.status_code, 200)  # Check for successful update

    def test_update_listing_failure(self):
        listing_id = 999  # Using a non-existing ID to simulate failure
        data = {
            'price':20000,
            'name':"He who remains"
        }
        response = self.client.patch(f'/listings/{listing_id}', json=data)
        self.assertEqual(response.status_code, 404)  # Check for a failure (listing not found)

    def test_delete_listing_success(self):
        listing_id = 1  # Replace with an existing listing ID
        response = self.client.delete(f'/listings/{listing_id}')
        self.assertEqual(response.status_code, 200)  # Check for successful deletion

    def test_delete_listing_failure(self):
        listing_id = 999  # Using a non-existing ID to simulate failure
        response = self.client.delete(f'/listings/{listing_id}')
        self.assertEqual(response.status_code, 404)  # Check for a failure (listing not found)

if __name__ == '__main__':
    unittest.main()
