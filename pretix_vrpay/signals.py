from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.signals import register_payment_providers
from pretix.presale.signals import process_response

from pretix_oppwa.signals import (
    wrapped_signal_process_response as wrapped_signal_process_response,
)
from pretix_vrpay.payment import VRPaySettingsHolder


@receiver(register_payment_providers, dispatch_uid="payment_vrpay")
def register_payment_provider(sender, **kwargs):
    from .paymentmethods import payment_method_classes

    return payment_method_classes

@receiver(signal=process_response, dispatch_uid="payment_vrpay_middleware_resp")
def signal_process_response(sender, request: HttpRequest, response: HttpResponse, **kwargs):
    return wrapped_signal_process_response(VRPaySettingsHolder, sender, request, response, **kwargs)

