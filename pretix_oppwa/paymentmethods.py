from django import forms
from django.utils.translation import gettext_lazy as _

from .payment import OPPWAMethod, OPPWASettingsHolder, OPPWApaydirekt

payment_methods = [
    {
        'identifier': 'scheme',
        'type': 'meta',
        'method': '',
        'public_name': _('Credit card'),
        'verbose_name': _('Credit card')
    }, {
        'identifier': 'affirm',
        'type': 'other',
        'method': 'AFFIRM',
        'public_name': _('Affirm'),
        'verbose_name': _('Affirm')
    }, {
        'identifier': 'airplus',
        'type': 'scheme',
        'method': 'AIRPLUS',
        'public_name': _('Airplus'),
        'verbose_name': _('Airplus')
    }, {
        'identifier': 'alia',
        'type': 'scheme',
        'method': 'ALIA',
        'public_name': _('Alia'),
        'verbose_name': _('Alia')
    }, {
        'identifier': 'aliadebit',
        'type': 'scheme',
        'method': 'ALIADEBIT',
        'public_name': _('Alia Debit'),
        'verbose_name': _('Alia Debit')
    }, {
        'identifier': 'amex',
        'type': 'scheme',
        'method': 'AMEX',
        'public_name': _('American Express'),
        'verbose_name': _('American Express')
    }, {
        'identifier': 'applepay',
        'type': 'scheme',
        'method': 'APPLEPAY',
        'public_name': _('Apple Pay'),
        'verbose_name': _('Apple Pay')
    }, {
        'identifier': 'argencard',
        'type': 'scheme',
        'method': 'ARGENCARD',
        'public_name': _('Argencard'),
        'verbose_name': _('Argencard')
    }, {
        'identifier': 'bcmc',
        'type': 'scheme',
        'method': 'BCMC',
        'public_name': _('BCMC'),
        'verbose_name': _('BCMC')
    }, {
        'identifier': 'carnet',
        'type': 'scheme',
        'method': 'CARNET',
        'public_name': _('Carnet'),
        'verbose_name': _('Carnet')
    }, {
        'identifier': 'cartebancaire',
        'type': 'scheme',
        'method': 'CARTEBANCAIRE',
        'public_name': _('Carte Bancaire'),
        'verbose_name': _('Carte Bancaire')
    }, {
        'identifier': 'cartebleue',
        'type': 'scheme',
        'method': 'CARTEBLEUE',
        'public_name': _('Carte Bleue'),
        'verbose_name': _('Carte Bleue')
    }, {
        'identifier': 'cencosud',
        'type': 'scheme',
        'method': 'CENCOSUD',
        'public_name': _('Cenco Sud'),
        'verbose_name': _('Cenco Sud')
    }, {
        'identifier': 'dankort',
        'type': 'scheme',
        'method': 'DANKORT',
        'public_name': _('Dankort'),
        'verbose_name': _('Dankort')
    }, {
        'identifier': 'diners',
        'type': 'scheme',
        'method': 'DINERS',
        'public_name': _('Diners Club'),
        'verbose_name': _('Diners Club')
    }, {
        'identifier': 'discover',
        'type': 'scheme',
        'method': 'DISCOVER',
        'public_name': _('Discovery'),
        'verbose_name': _('Discovery')
    }, {
        'identifier': 'elo',
        'type': 'scheme',
        'method': 'ELO',
        'public_name': _('ELO'),
        'verbose_name': _('ELO')
    }, {
        'identifier': 'facilypay_3x',
        'type': 'other',
        'method': 'FACILYPAY_3X',
        'public_name': _('3 Oney Installments'),
        'verbose_name': _('3 Oney Installments')
    }, {
        'identifier': 'facilypay_3xsansfrais',
        'type': 'other',
        'method': 'FACILYPAY_3XSANSFRAIS',
        'public_name': _('3 Oney Installments'),
        'verbose_name': _('3 Oney Installments (No Fees)')
    }, {
        'identifier': 'facilypay_4x',
        'type': 'other',
        'method': 'FACILYPAY_4X',
        'public_name': _('4 Oney Installments'),
        'verbose_name': _('4 Oney Installments')
    }, {
        'identifier': 'facilypay_4xsansfrais',
        'type': 'other',
        'method': 'FACILYPAY_4XSANSFRAIS',
        'public_name': _('4 Oney Installments'),
        'verbose_name': _('4 Oney Installments (No Fees)')
    }, {
        'identifier': 'googlepay',
        'type': 'scheme',
        'method': 'GOOGLEPAY',
        'public_name': _('Google Pay'),
        'verbose_name': _('Google Pay')
    }, {
        'identifier': 'hipercard',
        'type': 'scheme',
        'method': 'HIPERCARD',
        'public_name': _('Hipercard'),
        'verbose_name': _('Hipercard')
    }, {
        'identifier': 'jcb',
        'type': 'scheme',
        'method': 'JCB',
        'public_name': _('JCB'),
        'verbose_name': _('JCB')
    }, {
        'identifier': 'mada',
        'type': 'scheme',
        'method': 'MADA',
        'public_name': _('MADA'),
        'verbose_name': _('MADA')
    }, {
        'identifier': 'maestro',
        'type': 'scheme',
        'method': 'MAESTRO',
        'public_name': _('Maestro'),
        'verbose_name': _('Maestro')
    }, {
        'identifier': 'master',
        'type': 'scheme',
        'method': 'MASTER',
        'public_name': _('Mastercard'),
        'verbose_name': _('Mastercard')
    }, {
        'identifier': 'masterdebit',
        'type': 'scheme',
        'method': 'MASTERDEBIT',
        'public_name': _('Mastercard Debit'),
        'verbose_name': _('Mastercard Debit')
    }, {
        'identifier': 'mercadolivre',
        'type': 'scheme',
        'method': 'MERCADOLIVRE',
        'public_name': _('Mercado Livre'),
        'verbose_name': _('Mercado Livre')
    }, {
        'identifier': 'naranja',
        'type': 'scheme',
        'method': 'NARANJA',
        'public_name': _('Naranja'),
        'verbose_name': _('Naranja')
    }, {
        'identifier': 'nativa',
        'type': 'scheme',
        'method': 'NATIVA',
        'public_name': _('Nativa'),
        'verbose_name': _('Nativa')
    }, {
        'identifier': 'servired',
        'type': 'scheme',
        'method': 'SERVIRED',
        'public_name': _('Servired'),
        'verbose_name': _('Servired')
    }, {
        'identifier': 'tarjetashopping',
        'type': 'scheme',
        'method': 'TARJETASHOPPING',
        'public_name': _('Tarjeta Shopping'),
        'verbose_name': _('Tarjeta Shopping')
    }, {
        'identifier': 'tcard',
        'type': 'scheme',
        'method': 'TCARD',
        'public_name': _('TCard'),
        'verbose_name': _('TCard')
    }, {
        'identifier': 'tcarddebit',
        'type': 'scheme',
        'method': 'TCARDDEBIT',
        'public_name': _('TCard Debit'),
        'verbose_name': _('TCard Debit')
    }, {
        'identifier': 'unionpay',
        'type': 'scheme',
        'method': 'UNIONPAY',
        'public_name': _('UnionPay'),
        'verbose_name': _('UnionPay')
    }, {
        'identifier': 'unionpay_sms',
        'type': 'scheme',
        'method': 'UNIONPAY_SMS',
        'public_name': _('UnionPay (SMS)'),
        'verbose_name': _('UnionPay (SMS)')
    }, {
        'identifier': 'visa',
        'type': 'scheme',
        'method': 'VISA',
        'public_name': _('VISA'),
        'verbose_name': _('VISA')
    }, {
        'identifier': 'visadebit',
        'type': 'scheme',
        'method': 'VISADEBIT',
        'public_name': _('VISA Debit'),
        'verbose_name': _('VISA Debit')
    }, {
        'identifier': 'visaelectron',
        'type': 'scheme',
        'method': 'VISAELECTRON',
        'public_name': _('VISA Electron'),
        'verbose_name': _('VISA Electron')
    }, {
        'identifier': 'vpay',
        'type': 'scheme',
        'method': 'VPAY',
        'public_name': _('VPay'),
        'verbose_name': _('VPay')
    }, {
        'identifier': 'afterpay',
        'type': 'other',
        'method': 'AFTERPAY',
        'public_name': _('Afterpay'),
        'verbose_name': _('Afterpay')
    }, {
        'identifier': 'alipay',
        'type': 'other',
        'method': 'ALIPAY',
        'public_name': _('Alipay'),
        'verbose_name': _('Alipay')
    }, {
        'identifier': 'apostar',
        'type': 'other',
        'method': 'APOSTAR',
        'public_name': _('Apostar'),
        'verbose_name': _('Apostar')
    }, {
        'identifier': 'astropay_streamline_cash',
        'type': 'other',
        'method': 'ASTROPAY_STREAMLINE_CASH',
        'public_name': _('Astropay Streamline Cash'),
        'verbose_name': _('Astropay Streamline Cash')
    }, {
        'identifier': 'astropay_streamline_ot',
        'type': 'other',
        'method': 'ASTROPAY_STREAMLINE_OT',
        'public_name': _('Astropay Streamline OT'),
        'verbose_name': _('Astropay Streamline OT')
    }, {
        'identifier': 'baloto',
        'type': 'other',
        'method': 'BALOTO',
        'public_name': _('Baloto'),
        'verbose_name': _('Baloto')
    }, {
        'identifier': 'bancolombia',
        'type': 'other',
        'method': 'BANCOLOMBIA',
        'public_name': _('Bancolombia'),
        'verbose_name': _('Bancolombia')
    }, {
        'identifier': 'bbva_continental',
        'type': 'other',
        'method': 'BBVA_CONTINENTAL',
        'public_name': _('BBVA Continental'),
        'verbose_name': _('BBVA Continental')
    }, {
        'identifier': 'bcp',
        'type': 'other',
        'method': 'BCP',
        'public_name': _('BCP'),
        'verbose_name': _('BCP')
    }, {
        'identifier': 'bevalida',
        'type': 'other',
        'method': 'BEVALIDA',
        'public_name': _('Bevalida'),
        'verbose_name': _('Bevalida')
    }, {
        'identifier': 'boton_pse',
        'type': 'other',
        'method': 'BOTON_PSE',
        'public_name': _('Boton PSE'),
        'verbose_name': _('Boton PSE')
    }, {
        'identifier': 'caja_arequipa',
        'type': 'other',
        'method': 'CAJA_AREQUIPA',
        'public_name': _('Caja Arequipa'),
        'verbose_name': _('Caja Arequipa')
    }, {
        'identifier': 'caja_cusco',
        'type': 'other',
        'method': 'CAJA_CUSCO',
        'public_name': _('Caja Cusco'),
        'verbose_name': _('Caja Cusco')
    }, {
        'identifier': 'caja_huancayo',
        'type': 'other',
        'method': 'CAJA_HUANCAYO',
        'public_name': _('Caja Huancayo'),
        'verbose_name': _('Caja Huancayo')
    }, {
        'identifier': 'caja_ica',
        'type': 'other',
        'method': 'CAJA_ICA',
        'public_name': _('Caja ICA'),
        'verbose_name': _('Caja ICA')
    }, {
        'identifier': 'caja_piura',
        'type': 'other',
        'method': 'CAJA_PIURA',
        'public_name': _('Caja Piura'),
        'verbose_name': _('Caja Piura')
    }, {
        'identifier': 'caja_tacna',
        'type': 'other',
        'method': 'CAJA_TACNA',
        'public_name': _('Caja Tacna'),
        'verbose_name': _('Caja Tacna')
    }, {
        'identifier': 'caja_trujillo',
        'type': 'other',
        'method': 'CAJA_TRUJILLO',
        'public_name': _('Caja Trujillo'),
        'verbose_name': _('Caja Trujillo')
    }, {
        'identifier': 'cashu',
        'type': 'other',
        'method': 'CASHU',
        'public_name': _('Cashu'),
        'verbose_name': _('Cashu')
    }, {
        'identifier': 'chinaunionpay',
        'type': 'other',
        'method': 'CHINAUNIONPAY',
        'public_name': _('China Union Pay'),
        'verbose_name': _('China Union Pay')
    }, {
        'identifier': 'daopay',
        'type': 'other',
        'method': 'DAOPAY',
        'public_name': _('Daopay'),
        'verbose_name': _('Daopay')
    }, {
        'identifier': 'dimonex',
        'type': 'other',
        'method': 'DIMONEX',
        'public_name': _('Dimonex'),
        'verbose_name': _('Dimonex')
    }, {
        'identifier': 'efecty',
        'type': 'other',
        'method': 'EFECTY',
        'public_name': _('Efecty'),
        'verbose_name': _('Efecty')
    }, {
        'identifier': 'enterpay',
        'type': 'other',
        'method': 'ENTERPAY',
        'public_name': _('Enterpay'),
        'verbose_name': _('Enterpay')
    }, {
        'identifier': 'gana',
        'type': 'other',
        'method': 'GANA',
        'public_name': _('Gana'),
        'verbose_name': _('Gana')
    }, {
        'identifier': 'ikanooi_se',
        'type': 'other',
        'method': 'IKANOOI_SE',
        'public_name': _('Ikanooi Se'),
        'verbose_name': _('Ikanooi Se')
    }, {
        'identifier': 'inicis',
        'type': 'other',
        'method': 'INICIS',
        'public_name': _('Inicis'),
        'verbose_name': _('Inicis')
    }, {
        'identifier': 'interbank',
        'type': 'other',
        'method': 'INTERBANK',
        'public_name': _('Interbank'),
        'verbose_name': _('Interbank')
    }, {
        'identifier': 'klarna_payments_billpay',
        'type': 'other',
        'method': 'KLARNA_PAYMENTS_BILLPAY',
        'public_name': _('Klarna BillPay'),
        'verbose_name': _('Klarna BillPay')
    }, {
        'identifier': 'klarna_payments_paylater',
        'type': 'other',
        'method': 'KLARNA_PAYMENTS_PAYLATER',
        'public_name': _('Klarna Pay Later'),
        'verbose_name': _('Klarna Pay Later')
    }, {
        'identifier': 'klarna_payments_paynow',
        'type': 'other',
        'method': 'KLARNA_PAYMENTS_PAYNOW',
        'public_name': _('Klarna Pay Now'),
        'verbose_name': _('Klarna Pay Now')
    }, {
        'identifier': 'klarna_payments_sliceit',
        'type': 'other',
        'method': 'KLARNA_PAYMENTS_SLICEIT',
        'public_name': _('Klarna Slice It'),
        'verbose_name': _('Klarna Slice It')
    }, {
        'identifier': 'masterpass',
        'type': 'other',
        'method': 'MASTERPASS',
        'public_name': _('Masterpass'),
        'verbose_name': _('Masterpass')
    }, {
        'identifier': 'mbway',
        'type': 'other',
        'method': 'MBWAY',
        'public_name': _('MBWAY'),
        'verbose_name': _('MBWAY')
    }, {
        'identifier': 'moneybookers',
        'type': 'other',
        'method': 'MONEYBOOKERS',
        'public_name': _('Moneybookers'),
        'verbose_name': _('Moneybookers')
    }, {
        'identifier': 'moneysafe',
        'type': 'other',
        'method': 'MONEYSAFE',
        'public_name': _('Moneysafe'),
        'verbose_name': _('Moneysafe')
    }, {
        'identifier': 'nequi',
        'type': 'other',
        'method': 'NEQUI',
        'public_name': _('Nequi'),
        'verbose_name': _('Nequi')
    }, {
        'identifier': 'onecard',
        'type': 'other',
        'method': 'ONECARD',
        'public_name': _('Onecard'),
        'verbose_name': _('Onecard')
    }, {
        'identifier': 'pago_efectivo',
        'type': 'other',
        'method': 'PAGO_EFECTIVO',
        'public_name': _('Pago Efectivo'),
        'verbose_name': _('Pago Efectivo')
    }, {
        'identifier': 'pago_facil',
        'type': 'other',
        'method': 'PAGO_FACIL',
        'public_name': _('Pago Facil'),
        'verbose_name': _('Pago Facil')
    }, {
        'identifier': 'paybox',
        'type': 'other',
        'method': 'PAYBOX',
        'public_name': _('Paybox'),
        'verbose_name': _('Paybox')
    }, {
        'identifier': 'paydirekt',
        'type': 'other',
        'method': 'PAYDIREKT',
        'public_name': _('giropay'),
        'verbose_name': _('giropay (formerly paydirekt)'),
        'baseclass': OPPWApaydirekt,
        'help_text': '<div class="alert alert-danger">{}</div>'.format(
            _('{payment_method} payments only work if the customer fills in a full invoice address, so we recommend '
              'requiring an address in your invoicing settings.'.format(payment_method='giropay'))
        )
    }, {
        'identifier': 'paynet',
        'type': 'other',
        'method': 'PAYNET',
        'public_name': _('Paynet'),
        'verbose_name': _('Paynet')
    }, {
        'identifier': 'payolution_elv',
        'type': 'other',
        'method': 'PAYOLUTION ELV',
        'public_name': _('Payolution ELV'),
        'verbose_name': _('Payolution_ELV')
    }, {
        'identifier': 'payolution_ins',
        'type': 'other',
        'method': 'PAYOLUTION_INS',
        'public_name': _('Payolution INS'),
        'verbose_name': _('Payolution INS')
    }, {
        'identifier': 'payolution_invoice',
        'type': 'other',
        'method': 'PAYOLUTION_INVOICE',
        'public_name': _('Payolution Invoice'),
        'verbose_name': _('Payolution Invoice')
    }, {
        'identifier': 'paypal',
        'type': 'other',
        'method': 'PAYPAL',
        'public_name': _('PayPal'),
        'verbose_name': _('PayPal')
    }, {
        'identifier': 'paysafecard',
        'type': 'other',
        'method': 'PAYSAFECARD',
        'public_name': _('Paysafecard'),
        'verbose_name': _('Paysafecard')
    }, {
        'identifier': 'paytrail',
        'type': 'other',
        'method': 'PAYTRAIL',
        'public_name': _('Paytrail'),
        'verbose_name': _('Paytrail')
    }, {
        'identifier': 'pf_karte_direct',
        'type': 'other',
        'method': 'PF_KARTE_DIRECT',
        'public_name': _('PF Karte Direct'),
        'verbose_name': _('PF Karte Direct')
    }, {
        'identifier': 'przelewy',
        'type': 'other',
        'method': 'PRZELEWY',
        'public_name': _('Przelewy24'),
        'verbose_name': _('Przelewy24')
    }, {
        'identifier': 'punto_red',
        'type': 'other',
        'method': 'PUNTO_RED',
        'public_name': _('Punto Red'),
        'verbose_name': _('Punto Red')
    }, {
        'identifier': 'qiwi',
        'type': 'other',
        'method': 'QIWI',
        'public_name': _('Qiwi'),
        'verbose_name': _('Qiwi')
    }, {
        'identifier': 'rapi_pago',
        'type': 'other',
        'method': 'RAPI_PAGO',
        'public_name': _('Rapi Pago'),
        'verbose_name': _('Rapi Pago')
    }, {
        'identifier': 'ratenkauf',
        'type': 'other',
        'method': 'RATENKAUF',
        'public_name': _('Ratenkauf'),
        'verbose_name': _('Ratenkauf')
    }, {
        'identifier': 'red_servi',
        'type': 'other',
        'method': 'RED_SERVI',
        'public_name': _('Red Servi'),
        'verbose_name': _('Red Servi')
    }, {
        'identifier': 'scotiabank',
        'type': 'other',
        'method': 'SCOTIABANK',
        'public_name': _('Scotiabank'),
        'verbose_name': _('Scotiabank')
    }, {
        'identifier': 'sencillito',
        'type': 'other',
        'method': 'SENCILLITO',
        'public_name': _('Sencillito'),
        'verbose_name': _('Sencillito')
    }, {
        'identifier': 'shetab',
        'type': 'other',
        'method': 'SHETAB',
        'public_name': _('Shetab'),
        'verbose_name': _('Shetab')
    }, {
        'identifier': 'sibs_multibanco',
        'type': 'other',
        'method': 'SIBS_MULTIBANCO',
        'public_name': _('SIBS Multibanco'),
        'verbose_name': _('SIBS Multibanco')
    }, {
        'identifier': 'sofincosansfrais',
        'type': 'other',
        'method': 'SOFINCOSANSFRAIS',
        'public_name': _('Sofinco'),
        'verbose_name': _('Sofinco (No Fees)')
    }, {
        'identifier': 'stc_pay',
        'type': 'other',
        'method': 'STC_PAY',
        'public_name': _('STC Pay'),
        'verbose_name': _('STC Pay')
    }, {
        'identifier': 'su_red',
        'type': 'other',
        'method': 'SU_RED',
        'public_name': _('SU Red'),
        'verbose_name': _('SU Red')
    }, {
        'identifier': 'su_suerte',
        'type': 'other',
        'method': 'SU_SUERTE',
        'public_name': _('SU Suerte'),
        'verbose_name': _('SU Suerte')
    }, {
        'identifier': 'tenpay',
        'type': 'other',
        'method': 'TENPAY',
        'public_name': _('Tenpay'),
        'verbose_name': _('Tenpay')
    }, {
        'identifier': 'trustly',
        'type': 'other',
        'method': 'TRUSTLY',
        'public_name': _('Trustly'),
        'verbose_name': _('Trustly')
    }, {
        'identifier': 'wechat_pay',
        'type': 'other',
        'method': 'WECHAT_PAY',
        'public_name': _('Wechat Pay'),
        'verbose_name': _('Wechat Pay')
    }, {
        'identifier': 'western_union',
        'type': 'other',
        'method': 'WESTERN_UNION',
        'public_name': _('Western Union'),
        'verbose_name': _('Western Union')
    }, {
        'identifier': 'yandex',
        'type': 'other',
        'method': 'YANDEX',
        'public_name': _('Yandex'),
        'verbose_name': _('Yandex')
    }, {
        'identifier': 'bitcoin',
        'type': 'other',
        'method': 'BITCOIN',
        'public_name': _('Bitcoin'),
        'verbose_name': _('Bitcoin')
    }, {
        'identifier': 'boleto',
        'type': 'other',
        'method': 'BOLETO',
        'public_name': _('Boleto'),
        'verbose_name': _('Boleto')
    }, {
        'identifier': 'directdebit_sepa',
        'type': 'other',
        'method': 'DIRECTDEBIT_SEPA',
        'public_name': _('SEPA Direct Debit'),
        'verbose_name': _('SEPA Direct Debit')
    }, {
        'identifier': 'entercash',
        'type': 'other',
        'method': 'ENTERCASH',
        'public_name': _('Entercash'),
        'verbose_name': _('Entercash')
    }, {
        'identifier': 'eps',
        'type': 'other',
        'method': 'EPS',
        'public_name': _('eps'),
        'verbose_name': _('eps')
    }, {
        'identifier': 'giropay',
        'type': 'other',
        'method': 'GIROPAY',
        'public_name': _('giropay'),
        'verbose_name': _('giropay'),
        'help_text': '<div class="alert alert-danger">{}</div>'.format(
            _('giropay has been acquired by paydirekt. During the course of the acquisition, the phasing out of the '
              'existing giropay-system has been announced. Since December 2022, some payment providers started using '
              'the paydirekt system exclusively, but rebranded it from paydirekt to "the new giropay". Please contact '
              'your payment provider to learn more about this change and if you need to update your acceptance '
              'contract and/or integration. You might also want to consider disabling this payment method and enabling '
              '"giropay (formerly paydirekt)" instead.')
        )
    }, {
        'identifier': 'ideal',
        'type': 'other',
        'method': 'IDEAL',
        'public_name': _('iDEAL'),
        'verbose_name': _('iDEAL')
    }, {
        'identifier': 'interac_online',
        'type': 'other',
        'method': 'INTERAC_ONLINE',
        'public_name': _('Interac Online'),
        'verbose_name': _('Interac Online')
    }, {
        'identifier': 'oxxo',
        'type': 'other',
        'method': 'OXXO',
        'public_name': _('OXXO'),
        'verbose_name': _('OXXO')
    }, {
        'identifier': 'poli',
        'type': 'other',
        'method': 'POLI',
        'public_name': _('Poli'),
        'verbose_name': _('Poli')
    }, {
        'identifier': 'prepayment',
        'type': 'other',
        'method': 'PREPAYMENT',
        'public_name': _('Prepayment'),
        'verbose_name': _('Prepayment')
    }, {
        'identifier': 'sadad',
        'type': 'other',
        'method': 'SADAD',
        'public_name': _('Sadad'),
        'verbose_name': _('Sadad')
    }, {
        'identifier': 'sepa',
        'type': 'other',
        'method': 'SEPA',
        'public_name': _('SEPA'),
        'verbose_name': _('SEPA')
    }, {
        'identifier': 'sofortueberweisung',
        'type': 'other',
        'method': 'SOFORTUEBERWEISUNG',
        'public_name': _('Sofortüberweisung'),
        'verbose_name': _('Sofortüberweisung')
    }, {
        'identifier': 'trustpay_va',
        'type': 'other',
        'method': 'TRUSTPAY_VA',
        'public_name': _('Trustpay VA'),
        'verbose_name': _('Trustpay VA')
    }
]


def get_payment_method_classes(brand, payment_methods, baseclass, settingsholder, unique_entity_id=True):
    settingsholder.payment_methods_settingsholder = []
    for m in payment_methods:
        # We do not want meta methods like "scheme" in the settings holder
        if m['type'] == 'meta':
            continue
        settingsholder.payment_methods_settingsholder.append(
            ('method_{}'.format(m['method']),
             forms.BooleanField(
                label='{} {}'.format(
                    '<span class="fa fa-credit-card"></span>' if m['type'] == 'scheme' else '',
                    m['verbose_name']
                ),
                help_text=m['help_text'] if 'help_text' in m else '',
                required=False,
            ))
        )

        # All payment methods except the meta-Type "scheme" get their own EntityId Input
        # If there is only a single, unique EntityId, we skip this, too.
        if not settingsholder.unique_entity_id and m['type'] != 'scheme':
            settingsholder.payment_methods_settingsholder.append(
                ('entityId_{}'.format(m['method']),
                 forms.CharField(
                     label='{} ({})'.format(_('Entity ID'), m['verbose_name']),
                     required=False,
                     widget=forms.TextInput(
                         attrs={
                             'data-display-dependency': '#id_payment_{brand}_method_{method}'.format(
                                 brand=brand.lower(),
                                 method=m['method'],
                             )
                         }
                     ),
                 )),
            )

    # We do not want the "scheme"-methods listed as a payment-method, since they are covered by the meta methods
    return [settingsholder] + [
        type(
            f'OPPWA{"".join(m["public_name"].split())}', (
                # Custom baseclasses should always inherit from the brand-specific baseclass
                type(
                    f'OPPWA{"".join(m["public_name"].split())}',
                    (m["baseclass"], baseclass),
                    {}
                ) if 'baseclass' in m else baseclass,
            ), {
                'identifier': '{payment_provider}_{payment_method}'.format(
                    payment_method=m['identifier'],
                    payment_provider=brand.lower()
                ),
                'verbose_name': _('{payment_method} via {payment_provider}').format(
                    payment_method=m['verbose_name'], payment_provider=brand
                ),
                'public_name': m['public_name'],
                'method': m['method'],
                'type': m['type']
            })
        for m in payment_methods if m['type'] != 'scheme'
    ]


payment_method_classes = get_payment_method_classes('OPPWA', payment_methods, OPPWAMethod, OPPWASettingsHolder)
