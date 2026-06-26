import logging

from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from pretix.base.models import OrderPayment

from pretix_oppwa.payment import (
    OPPWAMethod as SuperOPPWAMethod, OPPWASettingsHolder,
)

logger = logging.getLogger("pretix_hobex")


class HobexSettingsHolder(OPPWASettingsHolder):
    identifier = "hobex_settings"
    verbose_name = _("Hobex")
    is_enabled = False
    is_meta = True
    unique_entity_id = True


class OPPWAMethod(SuperOPPWAMethod):
    identifier = "hobex"

    def get_merchant_transaction_id(self, payment):
        # For scheme-payments, Hobex only supports a 20 digit transaction ID, deviating from the OPPWA-standard.
        # For ease of use, we will not only follow this for scheme-transactions but for all transactions processed
        # through Hobex.
        return str(payment.pk).zfill(20)

    @property
    def additional_head(self):
        return get_template('pretix_hobex/pay_head.html').render()
