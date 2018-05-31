from enum import Enum

from nova_poshta.services.base_service import BaseService


class Status(Enum):
    CREATED = 'delivery created'
    DISPATCHED = 'delivery dispatched'
    ON_THE_WAY = 'delivery on the way'
    DELIVERED_TO_CITY = 'delivered to the destination city'
    DELIVERED = 'delivered to the warehouse'


class TrackingService(BaseService):

    def request(self):
        pass

    def get_status(self, id):
        pass

    @classmethod
    def validate_query_params(cls, body_params):
        required = ['warehouseRecipientRef', 'cost', 'amount']
        service_msg = 'track delivery status'
        try:
            cls._validate_query_params(body_params, required, service_msg)
        except ValueError as e:
            return str(e)
