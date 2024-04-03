from requests import get, post, delete


print(post('http://localhost:5000/api/v2/users/1', json={
    'nick_name': 'Tb',
    'number': '+79000000000',
    'email': 'zxc@gmail.com',
    'password': '123'
}).json())

print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())
