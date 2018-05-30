from nova_poshta.services.base_service import BaseService

from http.client import HTTPConnection
from nova_poshta import utils
import json


class DeliveryTimeService(BaseService):

    @classmethod
    def request(cls, query_params, headers):
        body = cls._build_request_body(query_params['cityRecipientRef'],
                                       query_params['date'])

        h1 = HTTPConnection(utils.NOVA_POSHTA_HOST)
        h1.request(method='POST', url=utils.NOVA_POSHTA_URL, headers=headers, body=bytes(body, encoding='utf-8'))

        response = h1.getresponse()
        response_body = json.loads(str(response.read(), 'utf-8'))
        h1.close()

        return cls._build_response(response_body)

    @staticmethod
    def _build_request_body(city_recipient_ref, date):
        return json.dumps(
            {
                "apiKey": utils.NOVA_POSHTA_API_KEY,
                "modelName": "InternetDocument",
                "calledMethod": "getDocumentDeliveryDate",
                "methodProperties": {
                    "DateTime": date,
                    "ServiceType": "WarehouseDoors",
                    "CitySender": utils.NOVA_POSHTA_KYIV_CITY_REF,
                    "CityRecipient": city_recipient_ref
                }
            }, ensure_ascii=False)

    @classmethod
    def validate_query_params(cls, query_params):
        required = ['cityRecipientRef', 'date']
        service_msg = 'evaluate expected arrival time'
        try:
            cls._validate_query_params(query_params, required, service_msg)
        except ValueError as e:
            return str(e)

    @staticmethod
    def _build_response(response_body):
        status = 200
        if not response_body['success']:
            status = 400
            return {'status': status, 'message': response_body['errors']}

        original_data = response_body['data'][0]

        new_response_data = {
            'expectedArrivalTime':
            {
                'date': original_data['DeliveryDate']['date'],
                'timezoneType': int(original_data['DeliveryDate']['timezone_type']),
                'timezone': original_data['DeliveryDate']['timezone']
            }
        }

        return {'status': status, 'data': new_response_data}
