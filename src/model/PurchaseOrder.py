class PurchaseOrder:
    id = ''
    purchase_order_id = ''
    latest = False
    created_at = ''
    acknowledged_at = ''
    requested_delivery_from = ''
    requested_delivery_to = ''
    currency = ''
    gross_amount = 0.0
    tax_amount = 0.0
    total_amount = 0.0
    is_partial_delivery = False
    sales_order = {}
    delivery_address = {}
    supplier = {}
    lines = {}

    def __init__(
            self, id, purchase_order_id, latest, created_at, acknowledged_at, requested_delivery_from,
            requested_delivery_to, currency, gross_amount, tax_amount, total_amount, is_partial_delivery,
            sales_order, delivery_address, supplier, lines
    ):
        self.lines = lines
        self.supplier = supplier
        self.delivery_address = delivery_address
        self.sales_order = sales_order
        self.is_partial_delivery = is_partial_delivery
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.gross_amount = gross_amount
        self.currency = currency
        self.requested_delivery_to = requested_delivery_to
        self.requested_delivery_from = requested_delivery_from
        self.acknowledged_at = acknowledged_at
        self.created_at = created_at
        self.latest = latest
        self.purchase_order_id = purchase_order_id
        self.id = id

    # Logic here in methods that checks that its
    # not possible to change the total, it should be calculated automatically
        

