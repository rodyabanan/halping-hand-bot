import requests
import json

def weather():
    URL = "https://api.weather.yandex.ru/v2/informers?lat=55.0457763671875&lon=82.9161148071289&lang=ru_RU"

    weather_translations = {
        'clear ' : 'ясно',
        'partly-cloudy' : 'малооблачно',
        'cloudy ' : 'облачно с прояснениями',
        'overcast' : 'пасмурно',
        'drizzle ' : 'морось',
        'light-rain' : 'небольшой дождь',
        'rain' : 'дождь',
        'moderate-rain': 'умеренно сильный дождь',
        'heavy-rain':'сильный дождь',
        'continuous-heavy-rain':'длительный сильный дождь',
        'showers':'ливень',
        'wet-snow':'дождь со снегом',
        'light-snow':'небольшой снег',
        'snow':'снег',
        'snow-showers':'снегопад',
        'hail':'град',
        'thunderstorm':'гроза',
        'thunderstorm-with-rain':'дождь с грозой',
        'thunderstorm-with-hail':'гроза с градом'
    }
    huy = {
        "X-Yandex-API-KEY": "token"
    }

    data = requests.get(URL, headers=huy)
    
    deserialized_data = json.loads(data.content)
    return  " \N{Sun Behind Cloud}Погода в Новосибирске {0} ℃, ощущается как {1} ℃\n\n\N{Wind Blowing Face}Скорость порывов ветра {2} м/c\n\n\N{Umbrella with Rain Drops}Погодное описание: {3}".format(deserialized_data['fact']['temp'], deserialized_data['fact']['feels_like'], deserialized_data['fact']['wind_gust'],weather_translations[deserialized_data['fact']['condition']])