from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nova_poshta.services.tracking_service import TrackingService
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
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 400, 'message': err})


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
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 400, 'message': err})


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
        headers = {'Content-Type': 'application/json'}

        err = TrackingService.validate_query_params(body)
        if not err:
            response = DeliveryService.create_delivery(body)

            if response['status'] == 200:
                return Response(status=status.HTTP_200_OK, headers=headers, data=response)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, headers=headers, data=response)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 400, 'message': err})


@api_view(['GET'])
def get_delivery_by_id(request, delivery_id):
    if request.method == 'GET':
        headers = {'Content-Type': 'application/json'}

        response = TrackingService.get_status(delivery_id)

        if response['status'] == 200:
            return Response(status=status.HTTP_200_OK, headers=headers, data=response)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data=response)
