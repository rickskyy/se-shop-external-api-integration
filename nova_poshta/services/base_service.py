from abc import ABC, abstractmethod


class BaseService(ABC):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def request(self, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def _validate_query_params(query_params, required, service_msg):
        for i in required:
            if i not in query_params:
                raise ValueError('Missing \'{i}\' param to complete {service} request'.format(i=i, service=service_msg))
