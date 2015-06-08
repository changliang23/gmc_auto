__author__ = 'lchang'

from suds.client import Client
from suds.transport.https import HttpAuthenticated

def TestWS():
    url = 'https://clvm060.asia.qagood.com:19005/PublicService?wsdl'
    client = Client(url)
    header = client.factory.create('Header')
    header.set = 'Authorization'
    value = client.factory.create('Value')
    value.set = 'Basic YXNpYVxzdmNiYW5nOnN2Yw=='
    client.set_options(soapheaders=(header, value))
    result = client.service.exportHandheldStatsNoWrapped('D07365FE-3649-4B8C-B352-DFE237F33596')

    print result

    __name__ == '__main__'
    TestWS()

