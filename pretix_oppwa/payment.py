import hashlib
import importlib
import json
import logging
import re
import requests
from collections import OrderedDict
from decimal import Decimal
from django import forms
from django.db import transaction
from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.models import Event, OrderPayment, OrderRefund
from pretix.base.payment import BasePaymentProvider, PaymentException
from pretix.base.settings import SettingsSandbox
from pretix.multidomain.urlreverse import eventreverse, build_absolute_uri

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
        if 'id' in payment.info_data:
            return True
        return False

    def payment_partial_refund_supported(self, payment: OrderPayment) -> bool:
        if 'id' in payment.info_data:
            return True
        return False

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

        self.process_result(refund, payment_info, 'execute_refund')

    def get_checkout_payload(self, payment: OrderPayment):
        ident = self.identifier.split('_')[0]

        return {
            'entityId': self.get_entity_id(payment.order.testmode),
            'amount': str(payment.amount),
            'currency': self.event.currency,
            'paymentType': 'DB',
            'merchantTransactionId': '{event}-{code}-P-{payment}'.format(event=self.event.slug.upper(), code=payment.order.code, payment=payment.local_id),
            # Ordinarily we would pass the type of payment method - or in the case of schemes all the allowed ones -
            # but somehow OPPWA only allows us to pass a single payment method. So we will not set it for credit cards.
            # 'paymentBrand': None if self.type == 'meta' else self.method
            'notificationUrl': build_absolute_uri(payment.order.event, 'plugins:pretix_{}:notify'.format(ident), kwargs={
                'order': payment.order.code,
                'payment': payment.pk,
                'hash': hashlib.sha1(payment.order.secret.lower().encode()).hexdigest(),
                'payment_provider': ident
            })
        }

    def create_checkout(self, payment: OrderPayment):
        s = self._init_api(payment.order.testmode)
        data = self.get_checkout_payload(payment)

        try:
            r = s.post(
                '{}/v1/checkouts'.format(self.get_endpoint_url(payment.order.testmode)),
                data=data,
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.exception('Error on creating payment: ' + str(e))
            payment.info = json.dumps(r.json())
            payment.save()

            raise PaymentException(
                _('We had trouble communicating with the payment service. Please try again and get '
                  'in touch with us if this problem persists.'))
        except requests.exceptions.RequestException as e:
            logger.exception('Error on creating payment: ' + str(e))
            raise PaymentException(
                _('We had trouble communicating with the payment service. Please try again and get '
                  'in touch with us if this problem persists.'))
        else:
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

    @transaction.atomic
    def process_result(self, payment_or_refund, data, datasource):
        if isinstance(payment_or_refund, OrderPayment):
            payment = payment_or_refund

            payment.order.log_action('pretix_oppwa.oppwa.event', data={
                'source': datasource,
                'data': data
            })

            # Successfully processed transactions
            if re.compile(r'^(000\.000\.|000\.100\.1|000\.[36])').match(data['result']['code']):
                if payment.state not in (OrderPayment.PAYMENT_STATE_CONFIRMED, OrderPayment.PAYMENT_STATE_REFUNDED):
                    payment.info_data = data
                    payment.save(update_fields=['info'])
                    payment.confirm()
            # Successfully processed transactions that should be manually reviewed
            elif re.compile(r'^(000\.400\.0[^3]|000\.400\.100)').match(data['result']['code']):
                if payment.state == OrderPayment.PAYMENT_STATE_CREATED:
                    payment.state = OrderPayment.PAYMENT_STATE_PENDING
                    payment.info_data = data
                    payment.save(update_fields=['state', 'info'])
            # Pending transaction in background, might change in 30 minutes or time out
            elif re.compile(r'^(000\.200)').match(data['result']['code']):
                if payment.state == OrderPayment.PAYMENT_STATE_CREATED:
                    payment.state = OrderPayment.PAYMENT_STATE_PENDING
                    payment.info_data = data
                    payment.save(update_fields=['state', 'info'])
            # Pending transaction in background, might change in some days or time out
            elif re.compile(r'^(800\.400\.5|100\.400\.500)').match(data['result']['code']):
                if payment.state == OrderPayment.PAYMENT_STATE_CREATED:
                    payment.state = OrderPayment.PAYMENT_STATE_PENDING
                    payment.info_data = data
                    payment.save(update_fields=['state', 'info'])
            else:
                if payment.state not in (OrderPayment.PAYMENT_STATE_CONFIRMED, OrderPayment.PAYMENT_STATE_REFUNDED):
                    payment.fail(info=data)

        elif isinstance(payment_or_refund, OrderRefund) and payment_or_refund.state in (
                OrderRefund.REFUND_STATE_CREATED, OrderRefund.REFUND_STATE_TRANSIT
        ):
            refund = payment_or_refund
            # We should really check here if there is a referenced id - but unfortuantely it is not always present...
            # if 'referencedId' not in data or refund.payment.info_data['id'] != data['referencedId']:
            if 'id' not in data:
                refund.state = OrderRefund.REFUND_STATE_FAILED
                refund.execution_date = now()

            # Successfully processed transactions
            if re.compile(r'^(000\.000\.|000\.100\.1|000\.[36])').match(data['result']['code']):
                refund.info_data = data
                refund.save(update_fields=['info'])
                refund.done()
            # Successfully processed transactions that should be manually reviewed
            elif re.compile(r'^(000\.400\.0[^3]|000\.400\.100)').match(data['result']['code']):
                refund.state = OrderRefund.REFUND_STATE_TRANSIT
                refund.info_data = data
                refund.save(update_fields=['state', 'info'])
            # Pending transaction in background, might change in 30 minutes or time out
            elif re.compile(r'^(000\.200)').match(data['result']['code']):
                refund.state = OrderRefund.REFUND_STATE_TRANSIT
                refund.info_data = data
                refund.save(update_fields=['state', 'info'])
            # Pending transaction in background, might change in some days or time out
            elif re.compile(r'^(800\.400\.5|100\.400\.500)').match(data['result']['code']):
                refund.state = OrderRefund.REFUND_STATE_TRANSIT
                refund.info_data = data
                refund.save(update_fields=['state', 'info'])
            else:
                refund.state = OrderRefund.REFUND_STATE_FAILED
                refund.execution_date = now()
                refund.info_data = data
                refund.save(update_fields=['state', 'execution_date', 'info'])
        else:
            raise PaymentException(_('We had trouble processing your transaction.'))


class OPPWApaydirekt(OPPWAMethod):
    def get_checkout_payload(self, payment: OrderPayment):
        payload = super().get_checkout_payload(payment)
        payload['shipping.street1'] = payment.order.invoice_address.street
        payload['shipping.city'] = payment.order.invoice_address.city
        payload['shipping.postcode'] = payment.order.invoice_address.zipcode
        payload['shipping.country'] = str(payment.order.invoice_address.country)
        payload['customer.givenName'] = payment.order.invoice_address.name_parts.get('given_name', payment.order.invoice_address.name)
        payload['customer.surname'] = payment.order.invoice_address.name_parts.get('family_name', payment.order.invoice_address.name)

        # We might also need to set the paymentBrand and shopperResultUrl - but when using testMode EXTERNAL, it also worked without.
        return payload

    def is_allowed(self, request: HttpRequest, total: Decimal = None) -> bool:
        return super().is_allowed(request, total) and request.event.settings.invoice_address_required
