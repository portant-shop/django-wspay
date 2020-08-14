from appconf import AppConf

from django.conf import settings  # noqa


class WSPayAppConf(AppConf):

    SUCCESS_URL = '/'
    ERROR_URL = '/'
    CANCEL_URL = '/'
    BASE_URL = None,
    DEVELOPMENT = None
    PAYMENT_ENDPOINT = None
    VERSION = '2.0'

    class Meta:
        prefix = 'ws_pay'
        required = ['SHOP_ID', 'SECRET_KEY']

    def configure(self):
        development = self.configured_data['DEVELOPMENT']

        # Set payment endpoint based on WS_PAY_DEVELOPMENT if it is not explicitly
        # set.
        if not self.configured_data['PAYMENT_ENDPOINT']:
            if development:
                payment_endpoint = 'https://formtest.wspay.biz/authorization.aspx'
            else:
                payment_endpoint = 'https://form.wspay.biz/authorization.aspx'
            self.configured_data['PAYMENT_ENDPOINT'] = payment_endpoint

        return self.configured_data

    def configure_development(self, value):
        return settings.DEBUG if value is None else value
