from requests import get, post, delete
from PIL import Image
from io import BytesIO
import base64


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
#     "type": "Clients",
#     "password": "zxc",
#     "email": "zxc1@g.com",
#     "nick_name": "zxc"
# }).json())

# print(delete('http://localhost:5000/api/v2/users/1').json())

# print(get('http://localhost:5000/api/v2/users').json())
#
# print(get('http://localhost:5000/api/v2/users/1').json())

# print(get('http://localhost:5000/api/v2/images/1').json())

# Image.open(BytesIO(base64.b64decode(get('http://localhost:5000/api/v2/images/1').json()['image']['data']))).show()

# with open('default.jpg', 'rb') as f:
#     print(post('http://localhost:5000/api/v2/images', json={
#         'data': base64.b64encode(f.read()).decode('utf-8'),
#         'master_id': 1,
#         'type': 'img'
#     }).json())

# print(post('http://localhost:5000/api/v2/images/3', json={
#     "type": "avatar"
# }).json())
