import requests

# Google Directions API калитини киритинг
api_key = 'AIzaSyDqiZx9bv1VK85IzCLSeXy9FvCjZeB-_bc'

# Манзилларни киритинг
origin = '42.30020238827357, 69.76079934783557'
destination = '42.31153616338686, 69.73558910463083'

# URL манзилини тайёрланг
url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=driving&key={api_key}'

# Сўровни юборинг
response = requests.get(url)

# Жавобни JSON форматида олинг
data = response.json()

# Жавобни кўрсатинг
if data['status'] == 'OK':
    route = data['routes'][0]
    legs = route['legs'][0]
    distance = legs['distance']['text']
    duration = legs['duration']['text']

    print(f"Umumiy masofa: {distance}")
    print(f"Umumiy вақт: {duration}")

    # Йўналиш бўйича қадамлар
    for step in legs['steps']:
        instruction = step['html_instructions']
        print(instruction)
else:
    print("Маршрут топилмади. Ишонч ҳосил қилинг манзиллар тўғри киритилган ва яна бир марта уриниб кўринг.")
