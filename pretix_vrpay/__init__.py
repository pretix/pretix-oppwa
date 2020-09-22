from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 3.11 or above to run this plugin!")

__version__ = '1.0.0'


class PluginApp(PluginConfig):
    name = 'pretix_vrpay'
    verbose_name = 'VR Payment payments for pretix'

    class PretixPluginMeta:
        name = gettext_lazy('VR Payment payments for pretix')
        author = 'Martin Gross'
        description = gettext_lazy('This plugin allows to use VR Payment as a payment provider')
        visible = True
        version = __version__
        category = 'PAYMENT'
        compatibility = "pretix>=3.10.0.dev0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_vrpay.PluginApp'
