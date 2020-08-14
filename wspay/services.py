from decimal import setcontext, Decimal, BasicContext
import hashlib

from django.urls import reverse

from wspay.conf import settings

EXP = Decimal('.01')
setcontext(BasicContext)


def process_data(incoming_data, request):
    """Process incoming data and prepare for POST to WSPay."""
    price = incoming_data['price']
    assert price > 0, 'Price must be greater than 0'
    total_for_sign, total = build_price(price)

    signature = generate_signature(
        [settings.WS_PAY_SHOP_ID, incoming_data['cart_id'], total_for_sign]
    )

    return_data = {
        'ShopID': settings.WS_PAY_SHOP_ID,
        'ShoppingCartID': incoming_data['cart_id'],
        'Version': settings.WS_PAY_VERSION,
        'TotalAmount': total,
        'Signature': signature,
        'ReturnURL': request.build_absolute_uri(
            reverse('wspay:process-response', kwargs={'status': 'success'})
        ),
        'CancelURL': request.build_absolute_uri(
            reverse('wspay:process-response', kwargs={'status': 'cancel'})
        ),
        'ReturnErrorURL': request.build_absolute_uri(
            reverse('wspay:process-response', kwargs={'status': 'error'})
        ),
    }

    return return_data


def generate_signature(param_list):
    """Compute the signature."""
    result = []
    for x in param_list:
        result.append(x)
        result.append(settings.WS_PAY_SECRET_KEY)
    return compute_hash(''.join(result))


def compute_hash(signature):
    """Compute the hash out of the given values."""
    return hashlib.sha512(signature.encode()).hexdigest()


def build_price(price):
    """
    Round to two decimals and return the tuple containing two variations of price.

    First element of the tuple is an int repr of price as as str 123.45 => '12345'
    Second element is a str that is a properly formatted price 00123.451 => '123,45'
    """
    rounded = price.quantize(EXP)
    _, digits, exp = rounded.as_tuple()

    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop

    for i in range(2):
        build(next() if digits else '0')
    build(',')
    if not digits:
        build('0')

    while digits:
        build(next())

    return str(int(rounded * 100)), ''.join(reversed(result))
