"""User Service"""

def create_user(user):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }

def get_users(filter=None):
    return [{
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }, {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }]

def get_user(user_id):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }

def update_user(user_id, user):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }

def delete_user(user_id):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }
