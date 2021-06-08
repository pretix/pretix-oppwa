from pretix_oppwa.paymentmethods import (
    get_payment_method_classes, payment_methods as payment_methods_repo,
)

from .payment import HobexSettingsHolder, OPPWAMethod

supported_methods = [
    # Meta-Scheme
    'SCHEME',

    # Scheme
    'MASTER',
    'VISA',
    'AMEX',
    'MASTERDEBIT',
    'MAESTRO',
    'VPAY',

    # Virtual Accounts
    'PAYPAL',

    # Bank Accounts
    'SOFORTUEBERWEISUNG',
    'DIRECTDEBIT_SEPA',
]
payment_methods = [item for item in payment_methods_repo if item.get('identifier').upper() in supported_methods]

payment_method_classes = get_payment_method_classes('Hobex', payment_methods, OPPWAMethod, HobexSettingsHolder)
