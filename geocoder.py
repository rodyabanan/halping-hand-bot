
from dadata import Dadata


def geo_lat(adr):
    token = "token"
    secret = "token"
    dadata = Dadata(token, secret)
    result = dadata.clean("address", adr)
    if not result['geo_lat']:
        return "Не могу найти такой адрес, попробуй еще раз :)"
    else:
        return result['geo_lat']

def geo_lon(adr):
    token = "token"
    secret = "token"
    dadata = Dadata(token, secret)
    result = dadata.clean("address", adr)
    return result['geo_lon']