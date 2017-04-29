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
