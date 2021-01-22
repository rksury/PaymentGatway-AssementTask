import re
import random
import json

from datetime import datetime
from dateutil import parser

from flask import Flask, Response
from flask import request

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


def PaymentGateway(amount):
    if amount < 20:
        msg = CheapPaymentGateway()
    elif 20 < amount > 500:
        msg = ExpensivePaymentGateway()
    else:
        msg = PremiumPaymentGateway()
    return msg


def PremiumPaymentGateway():
    for x in range(3):
        available = bool(random.getrandbits(1))
        if available is False:
            pass
        else:
            return 200
    return 500


def ExpensivePaymentGateway():
    available = bool(random.getrandbits(1))
    if not available:
        CheapPaymentGateway()
    else:
        return 200


def CheapPaymentGateway():
    available = bool(random.getrandbits(1))
    if available is False:
        return 500
    else:
        return 200


@app.route("/payment/", methods=["POST", ])
def ProcessPayment():
    data = json.loads(request.data.decode('utf-8'))
    pattern = re.compile(r'(?:\d{4}-){3}\d{4}|\d{16}')
    if not pattern.fullmatch(data.get('CreditCardNumber')) or not data.get('CreditCardNumber'):
        return Response("Please enter a valid credit card.", status=400)
    if not data.get('CardHolder') or (type(data.get('CardHolder')) is not str):
        return Response("this filed is required and must be string.", status=400)
    if not data.get('ExpirationDate') or parser.parse(data.get('ExpirationDate')) < datetime.now():
        return Response("credit card should not be expired.", status=400)
    if data.get('SecurityCode') and len(str(data.get('SecurityCode'))) > 3:
        return Response("Security code must have at least 3 integer.", status=400)
    if data.get('Amount') and data.get('Amount') < 0:
        return Response("Amount should be positive.", status=400)
    payment = PaymentGateway(data.get('Amount'))
    if payment == 200:
        return Response("Payment Successful", status=200)
    else:
        return Response("Payment failed", status=500)
