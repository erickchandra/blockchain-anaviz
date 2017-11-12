from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^price-realtime', views.priceRealtime, name="priceRealtime"),
    url(r'^ticker-blockchain', views.tickerBlockchain, name="tickerBlockchain"),
    url(r'^price-historical', views.priceHistorical, name="priceHistorical"),
    url(r'^price-exchange', views.priceExchange, name="priceExchange"),
    url(r'^ticker-bitfinex', views.tickerBitfinex, name="tickerBitfinex"),
    url(r'^ticker-kraken', views.tickerKraken, name="tickerKraken"),
    url(r'^depth-kraken', views.depthKraken, name="depthKraken"),
]