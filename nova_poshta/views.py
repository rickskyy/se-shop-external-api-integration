from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nova_poshta.services.city_list_service import CityListService
from nova_poshta.services.delivery_service import DeliveryService
from nova_poshta.services.warehouse_list_service import WarehouseListService


@api_view(['GET'])
def get_city_list_by_name(request):

    if request.method == 'GET':
        query_params = request.query_params
        err = CityListService.validate_query_params(query_params)

        if not err:
            headers = {'Content-Type': 'application/json'}

            response_body = CityListService.request(query_params, headers)

            if response_body['status'] == 200:
                return Response(status=status.HTTP_200_OK, headers=headers, data=response_body)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, headers=headers, data=response_body)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=err)


@api_view(['GET'])
def get_warehouse_list_by_city_name(request):
    if request.method == 'GET':
        query_params = request.query_params
        err = WarehouseListService.validate_query_params(query_params)

        if not err:
            headers = {'Content-Type': 'application/json'}

            response_body = WarehouseListService.request(query_params, headers)

            if response_body['status'] == 200:
                return Response(status=status.HTTP_200_OK, headers=headers, data=response_body)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, headers=headers, data=response_body)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=err)


@api_view(['GET', 'POST'])
def handle_delivery(request):
    if request.method == 'GET':
        query_params = request.query_params
        headers = {'Content-Type': 'application/json'}

        delivery_builder = DeliveryService()
        delivery = delivery_builder.build(query_params, headers)

        if delivery.status == 200:
            return Response(status=status.HTTP_200_OK, headers=headers, data=delivery.response)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=delivery.response)

    if request.method == 'POST':
        body = request.data

        delivery_service = DeliveryService()
        response = delivery_service.create_delivery(body)



