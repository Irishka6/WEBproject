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

# print(post('http://localhost:5000/api/v2/users', json={
#     'nick_name': 'qwerty',
#     'name': 'qwerty',
#     'surname': 'qwerty',
#     'number': '+79000000000',
#     'email': 'zxcc@gmail.com',
#     'password': '123',
#     'type': 'Masters',
#     'description': 'zxc',
#     'category': 1
# }).json())

print(delete('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())
