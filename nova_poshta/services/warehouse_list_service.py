from nova_poshta.services.base_service import BaseService

from http.client import HTTPConnection
from nova_poshta import utils
import json


class WarehouseListService(BaseService):

    @classmethod
    def request(cls, query_params, headers):
        body = cls._build_request_body(query_params['cityRef'])

        h1 = HTTPConnection(utils.NOVA_POSHTA_HOST)
        h1.request(method='POST', url=utils.NOVA_POSHTA_URL, headers=headers, body=bytes(body, encoding='utf-8'))

        response = h1.getresponse()
        response_body = json.loads(str(response.read(), 'utf-8'))
        h1.close()

        return cls._build_response(response_body)

    @staticmethod
    def _build_request_body(city_ref):
        return json.dumps({
                "modelName": "AddressGeneral",
                "calledMethod": "getWarehouses",
                "methodProperties": {
                  "CityRef": city_ref
                },
                "apiKey": utils.NOVA_POSHTA_API_KEY
        }, ensure_ascii=False)

    @classmethod
    def validate_query_params(cls, query_params):
        required = ['cityRef']
        service_msg = 'list warehouses'
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

        warehouse_list = []
        original_warehouses = response_body['data']

        for warehouse in original_warehouses:
            obj = {'description': warehouse['Description'],
                   'shortAddress': warehouse['ShortAddress'],
                   'ref': warehouse['Ref']}
            warehouse_list.append(obj)

        return {'status': status, 'data': warehouse_list}
