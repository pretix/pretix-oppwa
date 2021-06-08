import logging
from django.utils.translation import gettext_lazy as _
from pretix.base.models import OrderPayment

from pretix_oppwa.payment import (
    OPPWAMethod as SuperOPPWAMethod, OPPWASettingsHolder,
)

logger = logging.getLogger('pretix_hobex')


class HobexSettingsHolder(OPPWASettingsHolder):
    identifier = 'hobex_settings'
    verbose_name = _('Hobex')
    is_enabled = False
    is_meta = True
    unique_entity_id = True


class OPPWAMethod(SuperOPPWAMethod):
    identifier = 'hobex'

    def get_checkout_payload(self, payment: OrderPayment):
        data = super().get_checkout_payload(payment)

        # For scheme-payments, Hobex only supports a 20 digit transaction ID, deviating from the OPPWA-standard.
        # For ease of use, we will not only follow this for scheme-transactions but for all transactions processed
        # through Hobex.
        data['merchantTransactionId'] = str(payment.order.pk).zfill(20)

        return data
