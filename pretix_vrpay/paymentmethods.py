from pretix_oppwa.paymentmethods import (
    get_payment_method_classes, payment_methods as payment_methods_repo,
)

from .payment import OPPWAMethod, VRPaySettingsHolder

supported_methods = [
    # Meta-Scheme
    'SCHEME',

    # Scheme
    'AMEX',
    'DINERS',
    'JCB',
    'MASTER',
    'VISA',

    # Virtual Accounts
    'ENTERPAY',
    'KLARNA_PAYMENTS_PAYLATER',
    'KLARNA_PAYMENTS_SLICEIT',
    'PAYDIREKT',
    'PAYPAL',
    'RATENKAUF',

    # Bank Accounts
    'DIRECTDEBIT_SEPA',
    'GIROPAY',
    'SOFORTUEBERWEISUNG',
]
payment_methods = [item for item in payment_methods_repo if item.get('identifier').upper() in supported_methods]

payment_method_classes = get_payment_method_classes('VRPay', payment_methods, OPPWAMethod, VRPaySettingsHolder)
