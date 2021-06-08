import logging
from django.utils.translation import gettext_lazy as _

from pretix_oppwa.payment import (
    OPPWAMethod as SuperOPPWAMethod, OPPWASettingsHolder,
)

logger = logging.getLogger('pretix_vrpay')


class VRPaySettingsHolder(OPPWASettingsHolder):
    identifier = 'vrpay_settings'
    verbose_name = _('VR Payment')
    is_enabled = False
    is_meta = True
    unique_entity_id = False
    baseURLs = ['https://test.vr-pay-ecommerce.de', 'https://vr-pay-ecommerce.de']


class OPPWAMethod(SuperOPPWAMethod):
    identifier = 'vrpay'

    def get_endpoint_url(self, testmode):
        if testmode:
            return 'https://test.vr-pay-ecommerce.de'
        else:
            return 'https://vr-pay-ecommerce.de'
