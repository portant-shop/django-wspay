from django import forms
from django.core.exceptions import ValidationError


class UnprocessedPaymentForm(forms.Form):
    cart_id = forms.CharField()
    price = forms.DecimalField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    country = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)


class WSPaySignedForm(forms.Form):
    ShopID = forms.CharField(widget=forms.HiddenInput())
    ShoppingCartID = forms.CharField(widget=forms.HiddenInput())
    Version = forms.CharField(widget=forms.HiddenInput())
    TotalAmount = forms.CharField(widget=forms.HiddenInput())
    Signature = forms.CharField(widget=forms.HiddenInput())
    ReturnURL = forms.CharField(widget=forms.HiddenInput())
    CancelURL = forms.CharField(widget=forms.HiddenInput())
    ReturnErrorURL = forms.CharField(widget=forms.HiddenInput())
    ReturnMethod = forms.CharField(widget=forms.HiddenInput())

    # CUSTOMER DATA
    CustomerFirstName = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerLastName = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerAddress = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerCity = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerZIP = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerCountry = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerEmail = forms.CharField(required=False, widget=forms.HiddenInput())
    CustomerPhone = forms.CharField(required=False, widget=forms.HiddenInput())


class WSPayBaseResponseForm(forms.Form):
    ShoppingCartID = forms.CharField()
    Success = forms.IntegerField()
    ApprovalCode = forms.CharField(required=False)
    Signature = forms.CharField()


class WSPaySuccessErrorResponseForm(WSPayBaseResponseForm):
    CustomerFirstName = forms.CharField(required=False)
    CustomerSurname = forms.CharField(required=False)
    CustomerAddress = forms.CharField(required=False)
    CustomerCity = forms.CharField(required=False)
    CustomerZIP = forms.CharField(required=False)
    CustomerCountry = forms.CharField(required=False)
    CustomerPhone = forms.CharField(required=False)
    CustomerEmail = forms.CharField(required=False)
    Lang = forms.CharField(required=False)
    DateTime = forms.CharField(required=False)
    Amount = forms.CharField()
    ECI = forms.CharField(required=False)
    PaymentType = forms.CharField(required=False)
    PaymentPlan = forms.CharField(required=False)
    ShopPostedPaymentPlan = forms.CharField(required=False)
    ShopPostedLang = forms.CharField(required=False)
    ShopPostedCreditCardName = forms.CharField(required=False)
    ShopPostedPaymentMethod = forms.CharField(required=False)


class WSPaySuccessResponseForm(WSPaySuccessErrorResponseForm):
    STAN = forms.CharField(required=False)
    Partner = forms.CharField(required=False)
    WsPayOrderId = forms.CharField()
    CreditCardNumber = forms.CharField(required=False)
    ApprovalCode = forms.CharField()
    ErrorMessage = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['Success'] != 1 or cleaned_data['ApprovalCode'] == '':
            raise ValidationError(
                'Expecting success to be 1 and approval code to not be blank.'
            )


class WSPayErrorResponseForm(WSPaySuccessErrorResponseForm):
    ErrorMessage = forms.CharField()
    ErrorCodes = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['Success'] != 0:
            raise ValidationError('Expecting Success to be 0.')


class WSPayCancelResponseForm(WSPayBaseResponseForm):
    ResponseCode = forms.CharField()
