from nova_poshta.services.base_service import BaseService

from http.client import HTTPConnection
from nova_poshta import utils
import json


class DeliveryPriceService(BaseService):

    @classmethod
    def request(cls, query_params, headers):
        body = cls._build_request_body(query_params['cityRecipientRef'],
                                       query_params['cost'],
                                       query_params['amount'])

        h1 = HTTPConnection(utils.NOVA_POSHTA_HOST)
        h1.request(method='POST', url=utils.NOVA_POSHTA_URL, headers=headers, body=bytes(body, encoding='utf-8'))

        response = h1.getresponse()
        response_body = json.loads(str(response.read(), 'utf-8'))
        h1.close()

        return cls._build_response(response_body)

    @staticmethod
    def _build_request_body(city_recipient_ref, cost, amount):
        return json.dumps({
            "modelName": "InternetDocument",
            "calledMethod": "getDocumentPrice",
            "methodProperties": {
                "CitySender": utils.NOVA_POSHTA_KYIV_CITY_REF,
                "CityRecipient": city_recipient_ref,
                "Weight": 0.5,
                "ServiceType": "DoorsDoors",
                "Cost": cost,
                "CargoType": "Cargo",
                "SeatsAmount": amount
            },
            "apiKey": utils.NOVA_POSHTA_API_KEY
        }, ensure_ascii=False)

    @classmethod
    def validate_query_params(cls, query_params):
        required = ['cityRecipientRef', 'cost', 'amount']
        service_msg = 'calculate price'
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

        price = int(response_body['data'][0]['Cost'])

        return {'status': status, 'price': price}
