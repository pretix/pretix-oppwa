from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.urls import resolve
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.middleware import _merge_csp, _parse_csp, _render_csp
from pretix.base.signals import register_payment_providers, logentry_display
from pretix.presale.signals import process_response

from pretix_oppwa.payment import OPPWASettingsHolder


@receiver(register_payment_providers, dispatch_uid="payment_oppwa")
def register_payment_provider(sender, **kwargs):
    from .paymentmethods import payment_method_classes

    return payment_method_classes


@receiver(signal=process_response, dispatch_uid="payment_oppwa_middleware_resp")
def signal_process_response(sender, request: HttpRequest, response: HttpResponse, **kwargs):
    return wrapped_signal_process_response(OPPWASettingsHolder, sender, request, response, **kwargs)


def wrapped_signal_process_response(settingsholder, sender, request: HttpRequest, response: HttpResponse, **kwargs):
    provider = settingsholder(sender)
    url = resolve(request.path_info)

    if provider.settings.get('_enabled', as_type=bool) and "pay" in url.url_name:
        if 'Content-Security-Policy' in response:
            h = _parse_csp(response['Content-Security-Policy'])
        else:
            h = {}

        csps = {
            'script-src': provider.baseURLs + ['https://oppwa.com/', 'https://test.oppwa.com/', 'https://pay.google.com/', "'unsafe-eval'"],
            'style-src': provider.baseURLs + ['https://oppwa.com/', "'unsafe-inline'"],
            'connect-src': provider.baseURLs + ['https://oppwa.com/'],
            'img-src': provider.baseURLs + ['https://oppwa.com/', 'https://www.gstatic.com/'],
            'frame-src': provider.baseURLs + ['https://oppwa.com/', 'https://pay.google.com/', 'https:']
        }

        _merge_csp(h, csps)

        if h:
            response['Content-Security-Policy'] = _render_csp(h)
    return response


@receiver(signal=logentry_display, dispatch_uid="payment_oppwa_logentry_display")
def logentry_display(sender, logentry, **kwargs):
    if logentry.action_type != 'pretix_oppwa.oppwa.event':
        return

    return _('OPPWA reported an event')
