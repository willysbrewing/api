"""Responders"""

class Responder(object):

    def __init__(self, type, data):
        self.type = type
        if isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

    @property
    def serialize(self):
        # Empty data
        if len(self.data) == 1 and not self.data[0]:
            self.data.pop()
        def serialize_element(element):
            return {
                'id': element.pop('id', None),
                'type': self.type,
                'attributes': element
            }
        return [serialize_element(element) for element in self.data]


class UserResponder(Responder):
    def __init__(self, data):
        super(UserResponder, self).__init__(type='user', data=data)

class StockInfoResponder(Responder):
    def __init__(self, data):
        super(StockInfoResponder, self).__init__(type='stock_info', data=data)
