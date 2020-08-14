from django.dispatch import Signal

pay_request_created = Signal(providing_args=['instance'])
pay_request_updated = Signal(providing_args=['instance', 'status'])
