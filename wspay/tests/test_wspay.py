import pytest
import responses
import requests

from django.urls import reverse
from django.test.client import RequestFactory

from wspay.forms import UnprocessedPaymentForm, WSPaySignedForm
from wspay.models import WSPayRequest
from wspay.services import process_input_data, generate_signature

from django.conf import settings


def test_incoming_data_form():
    """Test the form that receives cart and user details."""
    form = UnprocessedPaymentForm()
    assert form.is_valid() is False
    form = UnprocessedPaymentForm({'user_id': 1, 'cart_id': 1, 'price': 1})
    assert form.is_valid()


@pytest.mark.django_db
def test_wspay_encode():
    """Test the processing function which prepares the data for WSPay."""
    assert settings.WS_PAY_SHOP_ID == 'ljekarnaplus'
    assert settings.WS_PAY_SECRET_KEY == '123456'

    return_data = {
        'ShopID': settings.WS_PAY_SHOP_ID,
        'Version': settings.WS_PAY_VERSION,
        'TotalAmount': '10,00',
        'ReturnURL': (
            'http://testserver' + reverse('wspay:process-response', kwargs={'status': 'success'})
        ),
        'CancelURL': (
            'http://testserver' + reverse('wspay:process-response', kwargs={'status': 'cancel'})
        ),
        'ReturnErrorURL': (
            'http://testserver' + reverse('wspay:process-response', kwargs={'status': 'error'})
        ),
        'ReturnMethod': 'POST',
    }

    incoming_form = UnprocessedPaymentForm({'cart_id': 1, 'price': 10})
    if (incoming_form.is_valid()):
        form_data = process_input_data(
            incoming_form.cleaned_data.copy(), RequestFactory().get('/')
        )

    req = WSPayRequest.objects.get()
    return_data['ShoppingCartID'] = str(req.request_uuid)
    return_data['Signature'] = generate_signature(
        [settings.WS_PAY_SHOP_ID, str(req.request_uuid), '1000']
    )

    assert return_data == form_data


@pytest.mark.django_db
def test_wspay_form():
    """Test the form that is used to make a WSPay POST request."""
    form = WSPaySignedForm()
    assert form.is_valid() is False

    incoming_form = UnprocessedPaymentForm({'user_id': 1, 'cart_id': 1, 'price': 1})
    if (incoming_form.is_valid()):
        form_data = process_input_data(
            incoming_form.cleaned_data.copy(),
            RequestFactory().get('/')
        )

    form = WSPaySignedForm(form_data)
    assert form.is_valid()
    form = form.cleaned_data

    responses.add(responses.POST, 'https://formtest.wspay.biz/authorization.aspx', status=200)
    response = requests.post('https://formtest.wspay.biz/authorization.aspx', form)
    assert response.status_code == 200
