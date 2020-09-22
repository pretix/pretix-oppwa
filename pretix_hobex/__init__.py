from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 3.11 or above to run this plugin!")

__version__ = '1.0.0'


class PluginApp(PluginConfig):
    name = 'pretix_hobex'
    verbose_name = 'Hobex payments for pretix'

    class PretixPluginMeta:
        name = gettext_lazy('Hobex payments for pretix')
        author = 'Martin Gross'
        description = gettext_lazy('This plugin allows to use Hobex as a payment provider')
        visible = True
        version = __version__
        category = 'PAYMENT'
        compatibility = "pretix>=3.10.0.dev0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_hobex.PluginApp'
