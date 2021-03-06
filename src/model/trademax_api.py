import datetime
import os
import pytz
import requests
import json

from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = ConfigParser()
parser.read(os.path.join(BASE_DIR, 'settings.ini'),)


class TrademaxAPI:
    """
    TrademaxAPI class to handle all API requests.
    """
    API_UUID = ''
    API_PASSWORD = ''
    API_URL = ''
    TOKEN = ''

    def __init__(self):
        self.API_UUID = parser.get('api', 'API_UUID')
        self.API_PASSWORD = parser.get('api', 'API_PASSWORD')
        self.API_URL = parser.get('api', 'API_URL')
        self.TOKEN = self.post_token_creation()

    def post_token_creation(self):
        """Returns a Bearer authentication token from the Trademax API."""
        r = requests.post(self.API_URL + '/jwt-token-get', data={
            'uuid': self.API_UUID,
            'password': self.API_PASSWORD
        })

        if r.status_code == 201:
            return r.headers['Authorization']
        else:
            return r.raise_for_status()

    def get_purchase_order(self, request_id):
        """Returns a single purchase order in JSON object."""
        r = requests.get(
            self.API_URL + '/purchase-order-requests/' + request_id,
            headers={'Authorization': self.TOKEN}
        )

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            return r.raise_for_status()

    def get_purchase_orders(self, page_no):
        """Gets all purchase orders by doing a GET request."""
        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        now_datetime = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        months_back = now - datetime.timedelta(weeks=24)
        months_back_datetime = months_back.strftime("%Y-%m-%dT%H:%M:%S%z")

        created_date_from = months_back_datetime
        created_date_to = now_datetime
        latest = 0 # TODO: Change this to 1 later
        per_page = 25
        sales_order_tenant = ''

        url = self.API_URL + '/purchase-order-requests'
        headers = {'Authorization': self.TOKEN}
        data = {
            'created_date_from': created_date_from,
            'created_date_to': created_date_to,
            'latest': latest,
            'per_page': per_page,
            'sales_order_tenant': sales_order_tenant,
            'page': page_no
        }
        r = requests.get(url, json=data, headers=headers).json()

        num_pages = r['pagination']['last_page']
        purchase_orders = []

        for d in r['data']:
            if d is not None:
                purchase_orders.append(d)

        return sorted(purchase_orders, key=lambda k: k['id'], reverse=True), num_pages

    def post_purchase_order_acknowledgement(self, request_id):
        """Sends an acknowledgement for one purchase order by doing a POST request."""
        now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
        date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")

        url = self.API_URL + '/purchase-order-acknowledgements'
        data = {'request_id': request_id, 'acknowledged_at': date_and_time}
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201:
            return r
        else:
            return r.raise_for_status()

    def post_purchase_order_response(
            self, request_id, status, reason, external_reference, gross_amount, tax_amount,
            total_amount, confirmed_delivery_from, confirmed_delivery_to, lines=None
    ):
        """Sends a response to Trademax API if accepted, rejected or corrected."""

        url = self.API_URL + '/purchase-order-responses'
        data = {
            'request_id': request_id, 'status': status, 'reason': reason,
            'external_reference': external_reference, 'gross_amount': gross_amount, 'tax_amount': tax_amount,
            'total_amount': total_amount, 'confirmed_delivery_from': confirmed_delivery_from,
            'confirmed_delivery_to': confirmed_delivery_to, 'lines': lines
        }
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201:
            return r
        else:
            return r.raise_for_status()

    def post_purchase_order_dispatch(
            self, purchase_order_id, dispatch_date, delivery_date, lines,
            external_reference, carrier_reference, shipping_agent,
            shipping_agent_service, tracking_code, dispatch_address
    ):
        """Sends order dispatch by POST request to Trademax API."""

        url = self.API_URL + '/purchase-order-dispatch'
        data = {
            'purchase_order_id': purchase_order_id, 'dispatch_date': dispatch_date,
            'delivery_date': delivery_date, 'lines': lines, 'external_reference': external_reference,
            'carrier_reference': carrier_reference, 'shipping_agent': shipping_agent,
            'shipping_agent_service': shipping_agent_service, 'tracking_code': tracking_code,
            'dispatch_address': dispatch_address
        }
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201 or r.status_code == 200:
            return r
        else:
            return r.raise_for_status()

    def post_purchase_order_invoice(
            self, purchase_order_id, lines, external_reference, gross_amount,
            total_amount, tax_amount, invoice_date, due_date
    ):
        """Sends order invoice by POST request to Trademax API."""

        url = self.API_URL + '/purchase-order-dispatch'
        data = {
            'purchase_order_id': purchase_order_id, 'lines': lines,
            'external_reference': external_reference, 'gross_amount': gross_amount,
            'total_amount': total_amount, 'tax_amount': tax_amount,
            'invoice_date': invoice_date, 'due_date': due_date
        }
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201 or r.status_code == 200:
            return r
        else:
            return r.raise_for_status()
