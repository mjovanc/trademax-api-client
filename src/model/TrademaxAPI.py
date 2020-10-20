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
