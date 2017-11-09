from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trace_price$', views.trace_price, name="tracePrice"),
    url(r'^compare_price$', views.compare_price, name="comparePrice"),
    url(r'^exchange_activity$', views.exchange_activity, name="exchangeActivity"),
    url(r'^potential_attacks$', views.potential_attacks, name="potentialAttacks"),
    url(r'^inspect_address$', views.inspect_address, name="inspectAddress"),

]