import requests
import json
import geocoder

def taxi(lon, lat, endlat, endlon):

    api = f"https://taxi-routeinfo.taxi.yandex.net/taxi_info?rll={lon},{lat}~{endlon},{endlat}&clid=ak220902&apikey=key&class=econom"
    
    headers = {"Accept": "application/json"}
    
    res = requests.get(api, headers=headers)
    if res.status_code == 200:
        deserialized_data = json.loads(res.content)
        calc_min = deserialized_data['time'] / 60
        return "\N{Taxi}Стоимость: {0} рублей, длительность: {1} минут \n \nПримерная стоимость поездки по указанному маршруту по тарифу «Эконом». Цена может отличаться в связи со спросом и наличием свободных такси. Подробнее на taxi.yandex.ru".format(round(deserialized_data['options'][0]['price']),  round(calc_min))
    else:
        return "Неверно введеные данные, попробуйте еще раз\N{Face With One Eyebrow Raised}"