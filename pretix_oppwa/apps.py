from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = '1.0.0'


class PluginApp(PluginConfig):
    name = 'pretix_oppwa'
    verbose_name = 'OPPWA payments'

    class PretixPluginMeta:
        name = gettext_lazy('OPPWA payments')
        author = 'Martin Gross'
        description = gettext_lazy('Easily connect to any payment provider using OPPWA-based technology.')
        visible = True
        version = __version__
        category = 'PAYMENT'
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA

