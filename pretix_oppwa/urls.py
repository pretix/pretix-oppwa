from django.conf.urls import include, url

from .views import NotifyView, PayView, ReturnView


def get_event_patterns(brand):
    return [
        url(r'^(?P<payment_provider>{})/'.format(brand), include([
            url(r'^pay/(?P<order>[^/]+)/(?P<hash>[^/]+)/(?P<payment>[^/]+)/$', PayView.as_view(), name='pay'),
            url(r'^return/(?P<order>[^/]+)/(?P<hash>[^/]+)/(?P<payment>[^/]+)/$', ReturnView.as_view(), name='return'),
            url(r'^notify/(?P<order>[^/]+)/(?P<hash>[^/]+)/(?P<payment>[^/]+)/$', NotifyView.as_view(), name='notify'),
        ])),
    ]


event_patterns = get_event_patterns('oppwa')
