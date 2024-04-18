from requests import get, post, delete


# print(post('http://localhost:5000/api/v2/users', json={
#     'name': 'qwerty',
#     'surname': 'zxc',
#     'number': '+79010000000',
#     'email': 'zxcz@gmail.com',
#     'password': '1233',
#     'type': 'Clients',
#     'appointments_ids': ''
# }).json())

print(post('http://localhost:5000/api/v2/users', json={
    "type": "Clients",
    "password": "zxc",
    "email": "zxc1@g.com",
    "nick_name": "zxc"
}).json())

print(delete('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())
