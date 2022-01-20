TRANSACTION_REPORT = {
    'WsPayOrderId': '96a5f58f-764c-4640-90ea-591280893bff',
    'UniqueTransactionNumber': 46370,
    'Signature': ''.join([
        '719cbb3ea1edb3cde1bf839c39be2be9fc43f96d317f862007b341862e623870110c1e2b27d556394',
        'ae76543d18a10120f6f9ea9753af4086aca036ef75010c1'
    ]),
    'STAN': '38967',
    'ApprovalCode': '961792',
    'ShopID': 'MYSHOP',
    'ShoppingCartID': '1c731772-e407-45f8-b576-7e20b0e8642d',
    'Amount': 78,
    'CurrencyCode': 191,
    'ActionSuccess': '1',
    'Success': '1',
    'Authorized': '1',
    'Completed': '0',
    'Voided': '0',
    'Refunded': '0',
    'PaymentPlan': '0000',
    'Partner': 'Pbz',
    'OnSite': '1',
    'CreditCardName': 'AMEX',
    'CreditCardNumber': '377500*****1007',
    'ECI': '',
    'CustomerFirstName': 'John',
    'CustomerLastName': 'Doe',
    'CustomerAddress': 'Street address 10',
    'CustomerCity': 'City',
    'CustomerCountry': 'HR',
    'CustomerPhone': '0911111111111111',
    'CustomerZIP': '51000',
    'CustomerEmail': 'john@doe.com',
    'TransactionDateTime': '20200423102457',
    'IsLessThen30DaysFromTransaction': True,
    'CanBeCompleted': True,
    'CanBeVoided': True,
    'CanBeRefunded': False,
    'Token': '09bf3d95-7a57-43f3-873a-216467a39925',
    'TokenNumber': '1007',
    'ExpirationDate': '2006'
}

STATUS_CHECK_RESPONSE = {
    'WsPayOrderId': '4ae43ae9-af8f-4ddd-8a21-7864f9fe81fb',
    'UniqueTransactionNumber': 380037,
    'Signature': ''.join([
        'b511d2d573d4858dd685fe8c0e8c01a97df4a43470df97604c6d6cdaa5cb593547d98b9',
        '3333257763de0a3d18e56bfe40d45256ba1ed892a5205bec08562aff4',
    ]),
    'STAN': '128729',
    'ApprovalCode': '307006',
    'ShopID': 'LJEKPLUS',
    'ShoppingCartID': '5f9c3535-0c25-4f6b-a86a-819ca1b27eec',
    'Amount': 80.55,
    'CurrencyCode': 191,
    'ActionSuccess': '1',
    'Success': '1',
    'Authorized': '1',
    'Completed': '0',
    'Voided': '0',
    'Refunded': '0',
    'PaymentPlan': '0000',
    'Partner': 'Pbz',
    'OnSite': '1',
    'CreditCardName': 'VISA',
    'CreditCardNumber': '478561******0189',
    'ECI': '',
    'CustomerFirstName': 'Vedran',
    'CustomerLastName': 'Vojvoda',
    'CustomerAddress': 'Testna ulica 1',
    'CustomerCity': 'Zagreb',
    'CustomerCountry': 'HR',
    'CustomerPhone': '55512345',
    'CustomerZIP': '10000',
    'CustomerEmail': 'vedran@pinkdroids.com',
    'TransactionDateTime': '20220119211635',
    'IsLessThen30DaysFromTransaction': True,
    'CanBeCompleted': True,
    'CanBeVoided': True,
    'CanBeRefunded': False,
    'ExpirationDate': '2212',
}


def secret_key():
    """Resolve secret key setting."""
    return 'MojSecret'


class MockResponse:
    def __init__(self, status_code, json_data):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
