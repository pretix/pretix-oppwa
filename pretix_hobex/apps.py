from django.utils.translation import gettext_lazy

from pretix_oppwa import __compatibility__, __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 3.11 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_hobex"
    verbose_name = "Hobex"

    class PretixPluginMeta:
        name = gettext_lazy("Hobex")
        author = "pretix Team"
        description = gettext_lazy(
            "Accept payments through Hobex, a payment provider active in Austria, Germany, "
            "Italia, and more european countries."
        )
        picture = "pretix_hobex/logo.png"
        visible = True
        version = __version__
        compatibility = "pretix>=2025.1.0.dev0"
        category = "PAYMENT"
        compatibility = __compatibility__

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_hobex.PluginApp"
