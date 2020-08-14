from decimal import setcontext, Decimal, BasicContext
import json
import hashlib

from django.core.exceptions import ValidationError
from django.urls import reverse

from wspay.conf import settings
from wspay.models import WSPayRequest
from wspay.signals import pay_request_created, pay_request_updated

EXP = Decimal('.01')
setcontext(BasicContext)


def process_input_data(input_data, request, user=None):
    """Process incoming data and prepare for POST to WSPay."""
    wspay_request = WSPayRequest.objects.create(
        cart_id=input_data['cart_id'],
    )
    # Send a signal
    pay_request_created.send_robust(WSPayRequest.__class__, instance=wspay_request)

    input_data['cart_id'] = str(wspay_request.request_uuid)

    price = input_data['price']
    assert price > 0, 'Price must be greater than 0'
    total_for_sign, total = build_price(price)

    signature = generate_signature(
        [settings.WS_PAY_SHOP_ID, input_data['cart_id'], total_for_sign]
    )

    return_data = {
        'ShopID': settings.WS_PAY_SHOP_ID,
        'ShoppingCartID': input_data['cart_id'],
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
        'ReturnMethod': 'POST',
    }
    if input_data.get('first_name'):
        return_data['CustomerFirstName'] = input_data['first_name']
    if input_data.get('last_name'):
        return_data['CustomerLastName'] = input_data['last_name']
    if input_data.get('address'):
        return_data['CustomerAddress'] = input_data['address']
    if input_data.get('city'):
        return_data['CustomerCity'] = input_data['city']
    if input_data.get('zip_code'):
        return_data['CustomerZIP'] = input_data['zip_code']
    if input_data.get('country'):
        return_data['CustomerCountry'] = input_data['country']
    if input_data.get('email'):
        return_data['CustomerEmail'] = input_data['email']
    if input_data.get('phone'):
        return_data['CustomerPhone'] = input_data['phone']

    return return_data


def verify_response(form_class, data):
    """Verify validity and authenticity of wspay response."""
    form = form_class(data=data)
    if form.is_valid():
        signature = form.cleaned_data['Signature']
        param_list = [
            settings.WS_PAY_SHOP_ID,
            data['ShoppingCartID'],
            data['Success'],
            data['ApprovalCode']
        ]
        expected_signature = generate_signature(param_list)
        if signature != expected_signature:
            raise ValidationError('Bad signature')

        return form.cleaned_data

    raise ValidationError('Form is not valid')


def process_response_data(response_data, request_status):
    """Update corresponding WSPayRequest object with response data."""
    wspay_request = WSPayRequest.objects.get(
        request_uuid=response_data['ShoppingCartID'],
    )
    wspay_request.status = request_status.name
    wspay_request.response = json.dumps(response_data)
    wspay_request.save()

    # Send a signal
    pay_request_updated.send_robust(
        WSPayRequest.__class__,
        instance=wspay_request,
        status=request_status
    )

    return wspay_request


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
