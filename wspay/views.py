import json

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View

from wspay.forms import (
    UnprocessedPaymentForm, WSPaySignedForm, WSPayErrorResponseForm, WSPaySuccessResponseForm,
    WSPayCancelResponseForm,
)
from wspay.models import WSPayRequest, WSPayRequestStatus
from wspay.services import process_data, generate_signature
from wspay.conf import settings


class ProcessView(FormView):
    """Receive payment data and prepare it for WSPay."""

    form_class = UnprocessedPaymentForm
    template_name = 'wspay/error.html'

    def form_valid(self, form):
        wspay_request = WSPayRequest.objects.create(
            cart_id=form.cleaned_data['cart_id'],
        )
        input_data = form.cleaned_data.copy()
        input_data['cart_id'] = str(wspay_request.request_uuid)

        form_data = process_data(input_data, self.request)
        wspay_form = WSPaySignedForm(form_data)
        return render(
            self.request,
            'wspay/wspay_submit.html',
            {'form': wspay_form, 'submit_url': settings.WS_PAY_PAYMENT_ENDPOINT}
        )


class PaymentStatus:
    SUCCESS = 'success'
    ERROR = 'error'
    CANCEL = 'cancel'


class ProcessResponseView(View):
    """Handle success, error and cancel."""

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        status = kwargs['status']
        assert status in [PaymentStatus.SUCCESS, PaymentStatus.ERROR, PaymentStatus.CANCEL]

        data = request.POST if request.method == 'POST' else request.GET
        if(status == PaymentStatus.SUCCESS):
            cleaned_data = self._verify_response(WSPaySuccessResponseForm, data)
            request_status = WSPayRequestStatus.COMPLETED
            redirect_url = settings.WS_PAY_SUCCESS_URL
            if cleaned_data['Success'] != 1 or cleaned_data['ApprovalCode'] == '':
                raise Exception('Expecting success to be 1 and approval code to not be blank.')
        elif(status == PaymentStatus.CANCEL):
            cleaned_data = self._verify_response(WSPayCancelResponseForm, data)
            request_status = WSPayRequestStatus.CANCELLED
            redirect_url = settings.WS_PAY_CANCEL_URL
        else:
            cleaned_data = self._verify_response(WSPayErrorResponseForm, data)
            request_status = WSPayRequestStatus.FAILED
            redirect_url = settings.WS_PAY_ERROR_URL
            if cleaned_data['Success'] != 0:
                raise Exception('Expecting Success to be 0.')

        wspay_request = WSPayRequest.objects.get(
            request_uuid=cleaned_data['ShoppingCartID'],
        )
        wspay_request.status = request_status.name
        wspay_request.response = json.dumps(cleaned_data)
        wspay_request.save()

        return redirect(redirect_url)

    def _verify_response(self, form_class, data):
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
                raise Exception('Bad signature')

            return form.cleaned_data

        raise Exception('Form is not valid')


class TestView(FormView):
    """Simple View to test the ProcessView."""

    template_name = 'wspay/test.html'
    form_class = UnprocessedPaymentForm
