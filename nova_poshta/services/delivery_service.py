from nova_poshta.models import Delivery
from nova_poshta.services.TrackingService import Status, TrackingService
from nova_poshta.services.delivery_price_service import DeliveryPriceService
from nova_poshta.services.delivery_time_service import DeliveryTimeService


class DeliveryResponseObject:
    def __init__(self):
        self.price = None
        self.expected_arrival_time = None
        self.errors = ''
        self.status = 200
        self.response = None
        self.city_recipient_ref = None
        self.city = None


class DeliveryService:

    def __init__(self):
        self.delivery = DeliveryResponseObject()
        self.err_price = None
        self.err_time = None

    def build(self, query_params, headers):
        if self._is_valid_query_params(query_params):
            if not self.err_price:
                response_body = DeliveryPriceService.request(query_params, headers)

                if response_body['status'] == 200:
                    self.delivery.price = response_body['price']
                else:
                    self.delivery.errors += ''.join(response_body['message']) + '\n'

            if not self.err_time:
                response_body = DeliveryTimeService.request(query_params, headers)

                if response_body['status'] == 200:
                    self.delivery.expected_arrival_time = response_body['data']
                else:
                    self.delivery.errors += ''.join(response_body['message']) + '\n'

            if not self.delivery.price and not self.delivery.expected_arrival_time:
                self.delivery.status = 400
                self._build_response_json()
            else:
                self._build_response_json()
        else:
            self.delivery.status = 400
            self._build_response_json()

        return self.delivery

    @staticmethod
    def create_delivery(request_body):
        delivery = Delivery(status=Status.CREATED, details=request_body)
        delivery.save()

        return {'status': 200, 'data': {'id': delivery.id}}

    def _is_valid_query_params(self, query_params):
        self.err_price = DeliveryPriceService.validate_query_params(query_params)
        self.err_time = DeliveryTimeService.validate_query_params(query_params)

        if self.err_price and self.err_time:
            self.delivery.errors += ''.join(self.err_price) + '\n'
            self.delivery.errors += ''.join(self.err_time) + '\n'
            return False

        if self.err_price:
            self.delivery.errors += ''.join(self.err_price) + '\n'

        if self.err_time:
            self.delivery.errors += ''.join(self.err_time) + '\n'

        return True

    def _build_response_json(self):
        if self.delivery.status == 200:
            if self.delivery.expected_arrival_time:
                expected_arrival_time = self.delivery.expected_arrival_time['expectedArrivalTime']
            else:
                expected_arrival_time = None
            self.delivery.response = {
                    'status': self.delivery.status,
                    'data':
                    {
                        'price': self.delivery.price,
                        'expectedArrivalTime': expected_arrival_time
                    },
                    'message': self.delivery.errors
                }
        elif self.delivery.status == 400:
            self.delivery.response = {
                    'status': self.delivery.status,
                    'message': self.delivery.errors
                }
