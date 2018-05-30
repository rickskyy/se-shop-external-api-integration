from nova_poshta.services.base_service import BaseService

from http.client import HTTPConnection
from nova_poshta import utils
import json


class CityListService(BaseService):

    @classmethod
    def request(cls, query_params, headers):
        body = cls._build_request_body(query_params['city'])

        h1 = HTTPConnection(utils.NOVA_POSHTA_HOST)
        h1.request(method='POST', url=utils.NOVA_POSHTA_URL, headers=headers, body=bytes(body, encoding='utf-8'))

        response = h1.getresponse()
        response_body = json.loads(str(response.read(), 'utf-8'))
        h1.close()

        return cls._build_response(response_body)

    @staticmethod
    def _build_request_body(city_name):
        return json.dumps({
            'apiKey': utils.NOVA_POSHTA_API_KEY,
            'modelName': 'Address',
            'calledMethod': 'searchSettlements',
            'methodProperties': {
                'CityName': city_name,
                'Limit': utils.NOVA_POSHTA_CITIES_LIMIT
            }
        }, ensure_ascii=False)

    @classmethod
    def validate_query_params(cls, query_params):
        required = ['city']
        service_msg = 'list cities'
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

        address_list = []
        original_addresses = response_body['data'][0]['Addresses']

        for address in original_addresses:
            obj = {'present': address['Present'],
                   'mainDescription': address['MainDescription'],
                   'area': address['Area'],
                   'settlementTypeCode': address['SettlementTypeCode'],
                   'parentRegionTypes': address['ParentRegionTypes'],
                   'parentRegionCode': address['ParentRegionCode'],
                   'deliveryCity': address['DeliveryCity']}
            address_list.append(obj)
        return {'status': status, 'data': address_list}
