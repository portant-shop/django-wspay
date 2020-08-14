from django import forms


class UnprocessedPaymentForm(forms.Form):
    user_id = forms.IntegerField()
    cart_id = forms.CharField()
    price = forms.DecimalField()


class WSPaySignedForm(forms.Form):
    ShopID = forms.CharField(widget=forms.HiddenInput())
    ShoppingCartID = forms.CharField(widget=forms.HiddenInput())
    Version = forms.CharField(widget=forms.HiddenInput())
    TotalAmount = forms.CharField(widget=forms.HiddenInput())
    Signature = forms.CharField(widget=forms.HiddenInput())
    ReturnURL = forms.CharField(widget=forms.HiddenInput())
    CancelURL = forms.CharField(widget=forms.HiddenInput())
    ReturnErrorURL = forms.CharField(widget=forms.HiddenInput())
