from enum import Enum
import random
from nova_poshta.models import Delivery
from nova_poshta.services.base_service import BaseService


class TrackingService(BaseService):

    def request(self):
        pass

    @classmethod
    def get_status(cls, id):
        try:
            delivery = Delivery.objects.get(pk=id)
        except Delivery.DoesNotExist:
            return {'status': 404, 'message': 'Delivery with the id does not exist'}

        curr_status = int(delivery.status)

        i = random.randint(0, 1)
        new_status_value = curr_status + i
        if new_status_value > 5:
            new_status_value = 5

        delivery.status = new_status_value
        delivery.save()

        return {'status': 200, 'data': {'deliveryStatus': cls.hack[new_status_value]}}

    @classmethod
    def validate_query_params(cls, body_params):
        required = ['warehouseRecipientRef', 'cost', 'amount']
        service_msg = 'track delivery status'
        try:
            cls._validate_query_params(body_params, required, service_msg)
        except ValueError as e:
            return str(e)

    hack = {1: 'delivery created', 2: 'delivery dispatched', 3: 'delivery on the way',
            4: 'delivered to the destination city', 5: 'delivered to the warehouse'}
