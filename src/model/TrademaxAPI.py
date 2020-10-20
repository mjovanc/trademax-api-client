import requests
import json


class TrademaxAPI:
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

    def post_purchase_order_response(self, response):
        """
        Use to send a response to the Trademax API if accepted, rejected or corrected.
        """

    def post_purchase_order_dispatch(self, obj):
        """
        Sends order dispatch by POST request to Trademax API.
        """
        pass

    def post_purchase_order_invoice(self, obj):
        """
        Sends order invoice by POST request to Trademax API.
        """
        pass

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
