from appconf import AppConf

from django.conf import settings  # noqa


class WSPayAppConf(AppConf):

    SUCCESS_URL = '/'
    ERROR_URL = '/'
    CANCEL_URL = '/'
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

    def configure_success_url(self, value):
        return self._configure_redirect_url(value)

    def configure_error_url(self, value):
        return self._configure_redirect_url(value)

    def configure_cancel_url(self, value):
        return self._configure_redirect_url(value)

    def _configure_redirect_url(self, value):
        # If redirect_url setting is a callable return it
        if hasattr(value, '__call__'):
            value

        # Try resolving the redirect_url to a fully qualified name
        # of a function, return the function object if found
        try:
            modname, part_symbol, attr = value.rpartition('.')
            assert part_symbol == '.'
            assert modname != ''
            m = __import__(modname, fromlist=[attr])
            f = getattr(m, attr)
            return f
        except Exception:
            pass

        return value
