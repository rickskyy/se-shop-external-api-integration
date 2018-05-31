from django.test import TestCase

# Create your tests here.
from nova_poshta.services.city_list_service import CityListService
import json


class CityServiceTestCase(TestCase):
    def setUp(self):
        self.query_params = {'wrong': 'київ'}
        self.response_body_false = {'success': False, 'errors': ''}
        self.response_body_true = {'success': True, 'data': [{'Addresses': ''}]}
        self.request_body = json.dumps({"apiKey": "a92fd8075e8131156225e7dd6d17b16e", "modelName": "Address", "calledMethod": "searchSettlements", "methodProperties": {"CityName": "київ", "Limit": 50}}, ensure_ascii=False)

    def test_validation(self):
        self.assertEqual("Missing 'city' param to complete list cities request", CityListService.validate_query_params(self.query_params))

    def test_build_response(self):
        self.assertEqual(400, CityListService._build_response(self.response_body_false)['status'])
        self.assertEqual(200, CityListService._build_response(self.response_body_true)['status'])

    def test_build_request_body(self):
        self.assertEqual(self.request_body, CityListService._build_request_body('київ'))
