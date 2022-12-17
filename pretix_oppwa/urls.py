from django.urls import include, path, re_path

from .views import NotifyView, PayView, ReturnView


def get_event_patterns(brand):
    return [
        re_path(r'^(?P<payment_provider>{})/'.format(brand), include([
            path('pay/<str:order>/<str:hash>/<str:payment>/', PayView.as_view(), name='pay'),
            path('return/<str:order>/<str:hash>/<str:payment>/', ReturnView.as_view(), name='return'),
            path('notify/<str:order>/<str:hash>/<str:payment>/', NotifyView.as_view(), name='notify'),
        ])),
    ]


event_patterns = get_event_patterns('oppwa')
