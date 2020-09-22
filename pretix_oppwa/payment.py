import importlib
import re

import hashlib
import json
import logging
from collections import OrderedDict
from decimal import Decimal

import requests
from django import forms
from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _  # NoQA

from pretix.base.models import Event, Order, OrderPayment, OrderRefund
from pretix.base.payment import BasePaymentProvider, PaymentException
from pretix.base.settings import SettingsSandbox
from pretix.multidomain.urlreverse import build_absolute_uri, eventreverse

logger = logging.getLogger('pretix_oppwa')


class OPPWASettingsHolder(BasePaymentProvider):
    identifier = 'oppwa_settings'
    verbose_name = _('OPPWA')
    is_enabled = False
    is_meta = True
    payment_methods_settingsholder = []
    unique_entity_id = True
    baseURLs = ['https://test.oppwa.com/', 'https://www.oppwa.com/']

    def __init__(self, event: Event):
        super().__init__(event)
        self.settings = SettingsSandbox('payment', self.identifier.split('_')[0], event)

    @property
    def settings_form_fields(self):
        fields = [
            ('access_token',
             forms.CharField(
                 label=_('Access Token'),
                 required=False,
             )),
            ('endpoint',
             forms.ChoiceField(
                 label=_('Endpoint'),
                 initial='live',
                 choices=(
                     ('live', 'Live'),
                     ('test', 'Test'),
                 ),
             )),
            ('entityId_scheme' if not self.unique_entity_id else 'entityId',
             forms.CharField(
                 label='{} ({})'.format(
                     _('Entity ID'),
                     _('Credit card') if not self.unique_entity_id else _('All Payment Methods')
                 ),
                 required=False,
             )),
        ]

        d = OrderedDict(
            fields + self.payment_methods_settingsholder + list(super().settings_form_fields.items())
        )
        d.move_to_end('_enabled', last=False)
        return d


class OPPWAMethod(BasePaymentProvider):
    identifier = ''
    method = ''
    type = ''

    def __init__(self, event: Event):
        super().__init__(event)
        self.settings = SettingsSandbox('payment', self.identifier.split('_')[0], event)

    @property
    def settings_form_fields(self):
        return {}

    @property
    def is_enabled(self) -> bool:
        if self.type == 'meta':
            module = importlib.import_module(
                __name__.replace('oppwa', self.identifier.split('_')[0]).replace('.payment', '.paymentmethods')
            )
            for method in list(filter(lambda d: d['type'] == 'scheme', module.payment_methods)):
                if self.settings.get('_enabled', as_type=bool) and self.settings.get(
                        'method_{}'.format(method['method']), as_type=bool):
                    return True
            return False
        else:
            return self.settings.get('_enabled', as_type=bool) and self.settings.get('method_{}'.format(self.method),
                                                                                 as_type=bool)

    def payment_refund_supported(self, payment: OrderPayment) -> bool:
        return True

    def payment_partial_refund_supported(self, payment: OrderPayment) -> bool:
        return True

    def get_endpoint_url(self, testmode):
        if testmode:
            return 'https://test.oppwa.com'
        else:
            return 'https://oppwa.com'

    def _init_api(self, testmode):
        s = requests.Session()
        s.headers = {
            'Authorization': 'Bearer {}'.format(self.settings.access_token)
        }

        return s

    def payment_control_render(self, request: HttpRequest, payment: OrderPayment):
        template = get_template('pretix_oppwa/control.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings,
               'payment_info': payment.info_data, 'order': payment.order, 'provname': self.verbose_name}
        return template.render(ctx)

    def refund_control_render(self, request: HttpRequest, payment: OrderPayment):
        template = get_template('pretix_oppwa/control.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings,
               'payment_info': payment.info_data, 'order': payment.order, 'provname': self.verbose_name}
        return template.render(ctx)

    def payment_form_render(self, request, **kwargs) -> str:
        template = get_template('pretix_oppwa/checkout_payment_form.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings}
        return template.render(ctx)

    def checkout_confirm_render(self, request) -> str:
        template = get_template('pretix_oppwa/checkout_payment_confirm.html')
        ctx = {'request': request, 'event': self.event, 'settings': self.settings}
        return template.render(ctx)

    def payment_pending_render(self, request, payment) -> str:
        if payment.info:
            payment_info = json.loads(payment.info)
        else:
            payment_info = None
        template = get_template('pretix_oppwa/pending.html')
        ctx = {
            'request': request,
            'event': self.event,
            'settings': self.settings,
            'provider': self,
            'order': payment.order,
            'payment': payment,
            'payment_info': payment_info,
            'payment_hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest()
        }
        return template.render(ctx)

    def checkout_prepare(self, request, total):
        return True

    def payment_is_valid_session(self, request):
        return True

    def is_allowed(self, request: HttpRequest, total: Decimal = None) -> bool:
        global_allowed = super().is_allowed(request, total)

        return global_allowed and self.get_entity_id(request.event.testmode)

    def get_entity_id(self, testmode):
        if (testmode and self.settings.endpoint == 'test') or (not testmode and self.settings.endpoint == 'live'):
            method = 'scheme' if self.type == 'meta' else self.method
            return self.settings.get(
                'entityId_{}'.format(method),
                self.settings.get('entityId', False)
            )
        else:
            return False

    def execute_payment(self, request: HttpRequest, payment: OrderPayment):
        ident = self.identifier.split('_')[0]
        return eventreverse(self.event, 'plugins:pretix_{}:pay'.format(ident), kwargs={
            'payment_provider': ident,
            'order': payment.order.code,
            'payment': payment.pk,
            'hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest(),
        })

    def execute_refund(self, refund: OrderRefund):
        payment_info = refund.payment.info_data
        if not payment_info:
            raise PaymentException(_('No payment information found.'))

        s = self._init_api(refund.order.testmode)
        data = {
            'entityId': self.get_entity_id(refund.order.testmode),
            'amount': str(refund.amount),
            'currency': self.event.currency,
            'paymentType': 'RF',
        }

        try:
            r = s.post(
                '{}/v1/payments/{}'.format(
                    self.get_endpoint_url(refund.order.testmode),
                    payment_info['id']
                ),
                data=data,
            )
        except requests.exceptions.RequestException as e:
            logger.exception('Error on creating refund: ' + str(e))
            raise PaymentException(
                _('We had trouble communicating with the payment service. Please try again and get '
                  'in touch with us if this problem persists.'))
        else:
            refund.info = json.dumps(r.json())
            refund.save()

        self.process_result(refund, payment_info)

    def create_checkout(self, payment: OrderPayment):
        s = self._init_api(payment.order.testmode)
        data = {
            'entityId': self.get_entity_id(payment.order.testmode),
            'amount': str(payment.amount),
            'currency': self.event.currency,
            'paymentType': 'DB',
            'merchantTransactionId': '{event}-{code}-P-{payment}'.format(event=self.event.slug.upper(), code=payment.order.code, payment=payment.local_id),
            # Ordinarily we would pass the type of payment method - or in the case of schemes all the allowed ones -
            # but somehow OPPWA only allows us to pass a single payment method. So we will not set it for credit cards.
            #'paymentBrand': None if self.type == 'meta' else self.method
        }

        try:
            r = s.post(
                '{}/v1/checkouts'.format(self.get_endpoint_url(payment.order.testmode)),
                data=data,
            )
        except requests.exceptions.RequestException as e:
            logger.exception('Error on creating payment: ' + str(e))
            raise PaymentException(
                _('We had trouble communicating with the payment service. Please try again and get '
                  'in touch with us if this problem persists.'))
        else:
            payment.info = json.dumps(r.json())
            payment.save()

            return '{}/v1/paymentWidgets.js?checkoutId={}'.format(
                self.get_endpoint_url(payment.order.testmode),
                r.json()['id']
            )

    def get_brands(self):
        if self.type == 'meta':
            module = importlib.import_module(
                __name__.replace('oppwa', self.identifier.split('_')[0]).replace('.payment', '.paymentmethods')
            )
            return ' '.join(x['method'] for x in list(filter(lambda d: d['type'] == 'scheme', module.payment_methods)))
        else:
            return self.method

    def process_result(self, payment, data):
        if payment.state in (
                OrderPayment.PAYMENT_STATE_PENDING, OrderPayment.PAYMENT_STATE_CREATED
        ):
            if 'id' not in data or 'id' not in payment.info_data or payment.info_data['id'] != data['id']:
                payment.fail()

            payment.info_data = data
            payment.save()

            # Successfully processed transactions
            if re.compile(r'^(000\.000\.|000\.100\.1|000\.[36])').match(data['result']['code']):
                payment.confirm()
            # Successfully processed transactions that should be manually reviewed
            if re.compile(r'^(000\.400\.0[^3]|000\.400\.100)').match(data['result']['code']):
                payment.state = OrderPayment.PAYMENT_STATE_PENDING
                payment.save()
            # Pending transaction in background, might change in 30 minutes or time out
            if re.compile(r'^(000\.200)').match(data['result']['code']):
                payment.state = OrderPayment.PAYMENT_STATE_PENDING
                payment.save()
            # Pending transaction in background, might change in some days or time out
            if re.compile(r'^(800\.400\.5|100\.400\.500)').match(data['result']['code']):
                payment.state = OrderPayment.PAYMENT_STATE_PENDING
                payment.save()
            else:
                payment.fail()
