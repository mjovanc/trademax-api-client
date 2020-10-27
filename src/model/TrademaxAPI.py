import requests
import json


class TrademaxAPI:
    """
    The TrademaxAPI class to handle all API requests.
    """

    API_UUID = '9f54693a-4608-4751-835a-d1e65265d187'
    API_PASSWORD = 'order@stenexpo.com'
    API_URL = 'http://api-231.trademax-test.com/v2'
    TOKEN = ''

    def __init__(self):
        self.TOKEN = self.post_token_creation()
        print(self.TOKEN) # remove later

    def post_token_creation(self):
        """
        Returns a Bearer authentication token from the Trademax API.
        """

        r = requests.post(self.API_URL + '/jwt-token-get', data={
            'uuid': self.API_UUID,
            'password': self.API_PASSWORD
        })

        if r.status_code == 201:
            return r.headers['Authorization']
        else:
            return r.raise_for_status()

    def get_purchase_order(self, request_id):
        """
        Returns a single purchase order in JSON object.
        """

        r = requests.get(
            self.API_URL + '/purchase-order-requests/' + request_id,
            headers={'Authorization': self.TOKEN}
        )

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            return r.raise_for_status()

    def get_purchase_order_list(self):
        """
        Gets all purchase orders by doing a GET request.
        """

        created_date_from = None
        created_date_to = None
        latest = 1
        per_page = 50
        sales_order_tenant = ''

        r = requests.get(self.API_URL + '/purchase-order-requests', headers={
            'Authorization': self.TOKEN
        }).json()

        num_pages = r['pagination']['last_page']
        print(r)

        for page in range(2, num_pages + 1):
            print('PAGE NUMBER : ' + str(page))

            new_req = requests.get(
                self.API_URL + '/purchase-order-requests',
                headers={'Authorization': self.TOKEN},
                params={'current_page': page}).json()

            for d in new_req['data']:
                if d is not None:
                    print(d)
                    # print(d['purchase_order_id'])

    def post_purchase_order_acknowledgement(self, request_id, acknowledged_at):
        """
        Sends an acknowledgement for one purchase order by doing a POST request.
        """

        url = self.API_URL + '/purchase-order-acknowledgements'
        data = {'request_id': request_id, 'acknowledged_at': acknowledged_at}
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201:
            return r
        else:
            return r.raise_for_status()

    def post_purchase_order_response(
            self, request_id, status, reason, external_reference, gross_amount, tax_amount,
            total_amount, confirmed_delivery_from, confirmed_delivery_to, lines
    ):
        """
        Use to send a response to the Trademax API if accepted, rejected or corrected.
        """

        url = self.API_URL + '/purchase-order-responses'
        data = {
            'request_id': request_id, 'status': status, 'reason': reason,
            'external_reference': external_reference, 'gross_amount': gross_amount, 'tax_amount': tax_amount,
            'total_amount': total_amount, 'confirmed_delivery_from': confirmed_delivery_from,
            'confirmed_delivery_to': confirmed_delivery_to, 'lines': lines
        }
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        print(data)

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201:
            return r
        else:
            print(r.text)
            return r.raise_for_status()

    def post_purchase_order_dispatch(
            self, purchase_order_id, dispatch_date, delivery_date, lines,
            external_reference, carrier_reference, shipping_agent,
            shipping_agent_service, tracking_code, dispatch_address
    ):
        """
        Sends order dispatch by POST request to Trademax API.
        """
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

        if r.status_code == 201:
            return r
        else:
            return r.raise_for_status()

    def post_purchase_order_invoice(
            self, purchase_order_id, lines, external_reference, gross_amount,
            total_amount, tax_amount, invoice_date, due_date
    ):
        """
        Sends order invoice by POST request to Trademax API.
        """
        url = self.API_URL + '/purchase-order-dispatch'
        data = {
            'purchase_order_id': purchase_order_id, 'lines': lines,
            'external_reference': external_reference, 'gross_amount': gross_amount,
            'total_amount': total_amount, 'tax_amount': tax_amount, 'invoice_date': invoice_date,
            'due_date': due_date
        }
        headers = {'Authorization': self.TOKEN, 'Content-Type': 'application/json'}

        r = requests.post(url, json=data, headers=headers)

        if r.status_code == 201:
            return r
        else:
            return r.raise_for_status()
