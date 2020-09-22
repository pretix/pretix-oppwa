import logging

from django.utils.translation import gettext_lazy as _

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
