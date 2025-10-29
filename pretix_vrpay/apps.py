from django.utils.translation import gettext_lazy

from pretix_oppwa import __compatibility__, __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 3.11 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_vrpay"
    verbose_name = "VR Payment"

    class PretixPluginMeta:
        name = gettext_lazy("VR Payment")
        author = "pretix Team"
        description = gettext_lazy(
            "Accept payments through VR Payment, the payment service provider of "
            "Volksbanken Raiffeisenbanken."
        )
        visible = True
        picture = "pretix_vrpay/logo.svg"
        version = __version__
        compatibility = "pretix>=2025.1.0.dev0"
        category = "PAYMENT"
        compatibility = __compatibility__

    def ready(self):
        from . import signals  # NOQA
