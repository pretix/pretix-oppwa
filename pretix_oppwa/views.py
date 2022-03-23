import hashlib
import requests
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _  # NoQA
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from pretix.base.models import Order, OrderPayment
from pretix.base.payment import PaymentException
from pretix.multidomain.urlreverse import build_absolute_uri, eventreverse


class OPPWAOrderView:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.order = request.event.orders.get(code=kwargs['order'])
            if hashlib.sha1(self.order.secret.lower().encode()).hexdigest() != kwargs['hash'].lower():
                raise Http404('Unknown order')
        except Order.DoesNotExist:
            # Do a hash comparison as well to harden timing attacks
            if 'abcdefghijklmnopq'.lower() == hashlib.sha1('abcdefghijklmnopq'.encode()).hexdigest():
                raise Http404('Unknown order')
            else:
                raise Http404('Unknown order')
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def pprov(self):
        return self.payment.payment_provider

    @property
    def payment(self):
        return get_object_or_404(
            self.order.payments,
            pk=self.kwargs['payment'],
            provider__istartswith=self.kwargs['payment_provider'],
        )

    def _redirect_to_order(self):
        return redirect(eventreverse(self.request.event, 'presale:event.order', kwargs={
            'order': self.order.code,
            'secret': self.order.secret
        }) + ('?paid=yes' if self.order.status == Order.STATUS_PAID else ''))


@method_decorator(xframe_options_exempt, 'dispatch')
class PayView(OPPWAOrderView, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        if self.payment.state not in [OrderPayment.PAYMENT_STATE_CREATED, OrderPayment.PAYMENT_STATE_PENDING]:
            return self._redirect_to_order()
        else:
            ctx = self.get_context_data()
            if ctx['checkouturl'] != 'fail':
                r = render(request, 'pretix_oppwa/pay.html', ctx)
                return r
            else:
                return self._redirect_to_order()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ident = self.pprov.identifier.split('_')[0]
        try:
            ctx['checkouturl'] = self.pprov.create_checkout(self.payment)
        except PaymentException:
            ctx['checkouturl'] = 'fail'
            messages.error(
                self.request,
                _('We had trouble communicating with the payment service. Please try again and get in touch with us if '
                  'this problem persists.')
            )
        ctx['order'] = self.order
        ctx['payment'] = self.payment
        ctx['payment_hash'] = hashlib.sha1(self.payment.order.secret.lower().encode()).hexdigest()
        ctx['brands'] = self.pprov.get_brands()
        ctx['returnurl'] = build_absolute_uri(self.request.event, 'plugins:pretix_{}:return'.format(ident), kwargs={
            'order': self.payment.order.code,
            'payment': self.payment.pk,
            'hash': hashlib.sha1(self.payment.order.secret.lower().encode()).hexdigest(),
            'payment_provider': ident
        })
        ctx['ident'] = ident
        return ctx


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(xframe_options_exempt, 'dispatch')
class ReturnView(OPPWAOrderView, View):
    viewsource = 'return_view'

    def get(self, request, *args, **kwargs):
        if 'resourcePath' not in request.GET:
            messages.error(self.request, _('Sorry, we could not validate the payment result. Please try again or '
                                           'contact the event organizer to check if your payment was successful.'))
            return self._redirect_to_order()

        s = self.pprov._init_api(self.payment.order.testmode)

        try:
            r = s.get(
                '{}{}?entityId={}'.format(
                    self.pprov.get_endpoint_url(self.payment.order.testmode),
                    request.GET['resourcePath'],
                    self.pprov.get_entity_id(self.payment.order.testmode),
                )
            )
        except requests.exceptions.RequestException:
            messages.error(self.request, _('Sorry, we could not validate the payment result. Please try again or '
                                           'contact the event organizer to check if your payment was successful.'))
            return self._redirect_to_order()
        else:
            try:
                self.pprov.process_result(self.payment, r.json(), self.viewsource)
            except PaymentException as e:
                messages.error(self.request, str(e))

        return self._redirect_to_order()


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(xframe_options_exempt, 'dispatch')
class NotifyView(ReturnView, OPPWAOrderView, View):
    viewsource = 'notify_view'

