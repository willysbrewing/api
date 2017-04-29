"""API errors"""


class Responder(object):

    def __init__(self, type, data):
        self.type = type
        self.data = data

    @property
    def serialize(self):
        return {
            'id': self.data.pop('id', None),
            'type': self.type,
            'attributes': self.data
        }


class UserResponder(Responder):
    def __init__(self, data):
        super(UserResponder, self).__init__(type='user', data=data)
